import os
import time
from pathlib import Path
from typing import Literal

import copy
import torch
from torch import nn

from ...tqdm import BTqdm
from ...writer import BWriter
from ...tools.text_style import BColor, BAppearance
from ..early_stop import BReloadByLoss
from ..early_stop import BStopByLoss, BStopByAcc
from ..early_stop import BStopByLossDelta, BStopByAccDelta
from ..early_stop import BStopByOverfitting
from ..early_stop import BStopByBYZH
from ...basic import Byzh

def inputs_function(inputs):
    return inputs
def outputs_function(outputs):
    return outputs
def labels_function(labels):
    return labels

class _saveDuringTrain:
    def __init__(self, path, rounds):
        self.path = path
        self.rounds = rounds
        self.cnt = 0
    def __call__(self):
        self.cnt += 1
        if self.cnt > self.rounds:
            self.cnt = 0
            return True
        return False

class BTrainer(Byzh):
    def __init__(
            self,
            model,
            train_loader,
            val_loader,
            optimizer,
            criterion,
            device,
            lrScheduler = None,
            isBinaryCls:bool = False,
            isParallel:bool = False,
            isSpikingjelly:bool = False):
        '''
        训练:\n
        train_eval_s\n
        训练前函数:\n
        load_model, load_optimizer, load_lrScheduler, set_writer, set_stop_by_acc\n
        训练后函数:\n
        save_latest_checkpoint, save_best_checkpoint, calculate_model
        :param model:
        :param train_loader:
        :param val_loader:
        :param optimizer:
        :param criterion:
        :param device:
        :param lrScheduler:
        :param isBinaryCls: 若是二分类, 则输出额外信息
        :param isParallel: 是否多GPU
        :param isSpikingjelly: 是否为SNN
        '''
        super().__init__()
        self.train_acc_lst = []
        self.train_loss_lst = []
        self.val_acc_lst = []
        self.val_f1_lst = []
        self.val_L0_True_lst = []
        self.val_L1_True_lst = []

        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.lrScheduler = lrScheduler
        self.isBinaryCls = isBinaryCls
        self.isParallel = isParallel
        self.isSpikingjelly = isSpikingjelly
        self.writer = None

        self.model.to(self.device)

        self._isTraining = False
        # save_temp
        self._save_during_train = None
        # early stop
        self._stop_by_acc = None
        self._stop_by_acc_delta = None
        self._stop_by_loss = None
        self._stop_by_loss_delta = None
        self._stop_by_overfitting = None
        self._stop_by_byzh = None
        # early reload
        self._reload_by_loss = None
        # save_best
        self._best_acc = 0
        self._best_model_state_dict = None
        self._best_optimizer_state_dict = None
        self._best_lrScheduler_state_dict = None

        if self.isParallel:
            if str(self.device) == str(torch.device("cuda")):
                if torch.cuda.device_count() > 1:
                    print(f"[set] 当前cuda数量:{torch.cuda.device_count()}, 使用多GPU训练")
                    self.model = nn.DataParallel(self.model)
                else:
                    print(f"[set] 当前cuda数量:{torch.cuda.device_count()}, 使用单GPU训练")

    def train_eval_s(
            self,
            epochs,
            inputs_func=inputs_function,
            outputs_func=outputs_function,
            labels_func=labels_function
    ):
        '''
        :param epochs:
        :param inputs_func: 对inputs的处理函数
        :param outputs_func: 对outputs的处理函数
        :param labels_func: 对labels的处理函数
        :return:
        '''
        self._isTraining = True

        # 检查inputs_func是否为函数
        if not callable(inputs_func):
            raise ValueError("inputs_func传入的参数应该要是一个函数!!!")
        # 检查outputs_func是否为函数
        if not callable(outputs_func):
            raise ValueError("outputs_func传入的参数应该要是一个函数!!!")
        # 检查labels_func是否为函数
        if not callable(labels_func):
            raise ValueError("labels_func传入的参数应该要是一个函数!!!")

        for epoch in range(epochs):
            train_acc, train_loss, current_lr = self._train_once(epoch, epochs, inputs_func, outputs_func, labels_func)
            val_acc = self._eval_once(inputs_func, outputs_func, labels_func)
            # 日志
            if self.writer is not None:
                self.writer.toFile(
                    f'Epoch [{epoch}/{epochs}], lr: {current_lr:.2e} | '
                    f'train_loss: {train_loss:.3f} | train_acc: {train_acc:.3f}, val_acc: {val_acc:.3f}'
                )
            # 保存模型
            if self._save_during_train is not None:
                if self._save_during_train():
                    self.save_best_checkpoint(self._save_during_train.path)
            # 早停
            if self._stop_by_acc is not None:
                if self._stop_by_acc(train_loss):
                    info = f'[stop] 模型在连续{self._stop_by_acc.rounds}个epoch内停滞, 触发stop_by_acc'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.cnt_list)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 早停
            if self._stop_by_acc_delta is not None:
                if self._stop_by_acc_delta(val_acc):
                    info = f'[stop] 模型在连续{self._stop_by_acc_delta.rounds}个epoch内过拟合, 触发stop_by_acc_delta'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.cnt_list)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 早停
            if self._stop_by_loss is not None:
                if self._stop_by_loss(train_loss):
                    info = f'[stop] 模型在连续{self._stop_by_loss.rounds}个epoch内停滞, 触发stop_by_loss'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.cnt_list)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 早停
            if self._stop_by_loss_delta is not None:
                if self._stop_by_loss_delta(train_loss):
                    info = f'[stop] 模型在连续{self._stop_by_loss_delta.rounds}个epoch内停滞, 触发stop_by_loss_delta'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.cnt_list)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 早停
            if self._stop_by_byzh is not None:
                if self._stop_by_byzh(train_loss, train_acc, val_acc):
                    info = f'[stop] 模型在连续{self._stop_by_byzh.rounds}个epoch内停滞, 触发stop_by_byzh'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.flags)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 过拟合
            if self._stop_by_overfitting is not None:
                if self._stop_by_overfitting(train_acc, val_acc):
                    info = f'[stop] 模型在连续{self._stop_by_overfitting.rounds}个epoch内过拟合, 触发stop_by_overfitting'
                    self._print_and_toWriter(info)
                    info = "[stop] " + str(self._stop_by_byzh.cnt_list)
                    self._print_and_toWriter(info, if_print=False)
                    break
            # 重加载
            if self._reload_by_loss is not None:
                match self._reload_by_loss(train_loss):
                    case 'continue':
                        pass
                    case 'reload':
                        info = f'模型触发reload_by_loss(第{self._reload_by_loss.cnt_reload}次加载)'
                        self._print_and_toWriter(info)
                        # 加载
                        self.model.load_state_dict(self._best_model_state_dict)
                        self.optimizer.load_state_dict(self._best_optimizer_state_dict)
                        if self.lrScheduler is not None:
                            self.lrScheduler.load_state_dict(self._best_lrScheduler_state_dict)
                        self.calculate_model()
                    case 'done':
                        pass
    def calculate_model(self, dataloader=None, model=None):
        '''
        如果不指定, 则用类内的
        :param dataloader: 默认self.val_loader
        :param model: 默认self.model
        :return:
        '''
        if dataloader==None:
            dataloader = self.val_loader
        if model==None:
            model = self.model
        model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        inference_time = []
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                start_time = time.time()
                outputs = model(inputs)
                end_time = time.time()
                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())
                inference_time.append(end_time - start_time)
                if self.isSpikingjelly:
                    from spikingjelly.activation_based import functional
                    functional.reset_net(model)
            # 平均推理时间
            inference_time = sum(inference_time) / len(inference_time)
            # acc & f1
            accuracy = correct / total
            f1_score = self._get_f1_score(y_true, y_pred)
            # 参数量
            params = sum(p.numel() for p in model.parameters())

            info = f'[calc] accuracy: {accuracy:.3f}, f1_score: {f1_score:.3f}'
            self._print_and_toWriter(info)
            info = f'------ inference_time: {inference_time:.2e}s, params: {params / 1e3}K'
            self._print_and_toWriter(info)

            if self.isBinaryCls:
                cm = self._get_confusion_matrix(y_true, y_pred)
                TN = cm[0, 0]
                FP = cm[0, 1]
                FN = cm[1, 0]
                TP = cm[1, 1]
                L0_True = self._get_L0_True(TN, FP)
                L1_True = self._get_L1_True(FN, TP)

                info = f'------ L0_True: {L0_True:.3f}, L1_True: {L1_True:.3f}'
                self._print_and_toWriter(info)

        return accuracy, f1_score, inference_time, params

    def save_latest_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'lrScheduler': self.lrScheduler.state_dict() if self.lrScheduler is not None else None
        }
        torch.save(checkpoint, path)
        print(f"[save] latest_checkpoint 已保存到 {path}")

    def save_best_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'model': self._best_model_state_dict,
            'optimizer': self._best_optimizer_state_dict,
            'lrScheduler': self._best_lrScheduler_state_dict
        }
        torch.save(checkpoint, path)
        print(f"[save] best_checkpoint 已保存到 {path}")
    def load_model(self, path):
        checkpoint = torch.load(path, map_location='cpu')
        self.model.load_state_dict(checkpoint['model'])
        self.model.to(self.device)
        print(f"[load] model 已从 {path} 加载")
    def load_optimizer(self, path):
        checkpoint = torch.load(path)
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        print(f"[load] optimizer 已从{path}加载")
    def load_lrScheduler(self, path):
        checkpoint = torch.load(path)
        if self.lrScheduler is not None and checkpoint['lrScheduler'] is not None:
            self.lrScheduler.load_state_dict(checkpoint['lrScheduler'])
            print(f"[load] lrScheduler 已从{path}加载")
        else:
            print(f"[load] path中的lrScheduler为None, 加载失败")

    def set_writer(self, path: Path, mode: Literal["a", "w"] = "a"):
        '''
        请在训练前设置set_writer
        '''
        self.writer = BWriter(path, ifTime=True)
        if mode == 'a':
            pass
        if mode == 'w':
            self.writer.clearFile()

        self.writer.toFile("[dataset] -> " + self.train_loader.dataset.__class__.__name__, ifTime=False)
        self.writer.toFile("[batch_size] -> " + str(self.train_loader.batch_size), ifTime=False)
        self.writer.toFile("[lr] -> " + str(self.optimizer.param_groups[0]['lr']), ifTime=False)
        self.writer.toFile("[criterion] -> " + str(self.criterion), ifTime=False)
        self.writer.toFile("[optimizer] -> " + str(self.optimizer), ifTime=False)
        if self.lrScheduler is not None:
            self.writer.toFile("[lrScheduler] -> " + str(self.lrScheduler), ifTime=False)
        self.writer.toFile("[model] -> " + str(self.model), ifTime=False)

        print(f'[set] 日志将保存到{path}')
    def set_save_during_train(self, path: Path, rounds=10):
        '''
        请在训练前设置set_save_during_train
        '''
        self._save_during_train = _saveDuringTrain(path, rounds)
        self._print_and_toWriter(f"[set] save_during_train")
    def set_stop_by_acc(self, rounds=10, delta=0.01):
        '''
        请在训练前设置set_stop_by_acc
        :param rounds: 连续rounds次, val_acc - max_val_acc > delta, 则停止训练
        '''
        self._stop_by_acc = BStopByAcc(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_acc")
    def set_stop_by_overfitting(self, rounds=10, delta=0.1):
        '''
        请在训练前设置set_stop_by_overfitting
        :param rounds: 连续rounds次, train_acc - val_acc > delta, 则停止训练
        '''
        self._stop_by_overfitting = BStopByOverfitting(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_overfitting")
    def set_stop_by_acc_delta(self, rounds=10, delta=0.003):
        '''
        请在训练前设置set_stop_by_acc_delta
        :param rounds: 连续rounds次, |before_acc - val_acc| <= delta, 则停止训练
        '''
        self._stop_by_acc_delta = BStopByAccDelta(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_acc_delta")
    def set_stop_by_loss(self, rounds=10, delta=0.01):
        '''
        请在训练前设置set_stop_by_loss
        :param rounds: 连续rounds次, train_loss - min_train_loss > delta, 则停止训练
        '''
        self._stop_by_loss = BStopByLoss(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_loss")
    def set_stop_by_loss_delta(self, rounds=10, delta=0.002):
        '''
        请在训练前设置set_stop_by_loss_delta
        :param rounds: 连续rounds次, |before_loss - now_loss| <= delta, 则停止训练
        '''
        self._stop_by_loss_delta = BStopByLossDelta(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_loss_delta")
    def set_stop_by_byzh(self, rounds=10, loss_delta=0.002, acc_delta=0.003):
        '''
        请在训练前设置set_stop_by_byzh
        '''
        self._stop_by_byzh = BStopByBYZH(rounds=rounds, loss_delta=loss_delta, acc_delta=acc_delta)
        self._print_and_toWriter(f"[set] stop_by_byzh")
    def set_reload_by_loss(self, max_reload_count=5, reload_rounds=10, delta=0.01):
        '''
        请在训练前设置set_reload_by_loss\n
        :param reload_rounds: 连续reload_rounds次都是train_loss > min_train_loss + delta
        '''
        self._reload_by_loss = BReloadByLoss(max_reload_count, reload_rounds, delta)
        self._print_and_toWriter(f"[set] reload_by_loss")

    def draw(self, jpg_path: Path, if_show=False):
        parent_path = Path(jpg_path).parent
        os.makedirs(parent_path, exist_ok=True)

        import matplotlib
        if if_show == False:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np  # 导入numpy库

        palette = sns.color_palette("Set2", 3)

        plt.figure(figsize=(8, 8))
        plt.subplots_adjust(hspace=0.4)

        plt.subplot(3, 1, 1)
        # 每十个画一次(防止点多卡顿)
        temp = [x for i, x in enumerate(self.train_loss_lst) if (i + 1) % 10 == 0]
        plt.plot(temp, color="red", label="train_loss")
        plt.xlabel("iter 1/10")
        plt.ylabel("loss")
        plt.legend(loc='upper right')

        plt.subplot(3, 1, 2)
        plt.plot(self.train_acc_lst, color="red", label="train_acc")
        plt.plot(self.val_acc_lst, color="blue", label="val_acc")
        # 找到train_acc的峰值点并标记
        train_acc_peak_index = np.argmax(self.train_acc_lst)
        plt.scatter(train_acc_peak_index, self.train_acc_lst[train_acc_peak_index], color="red", marker="v", s=100)
        # 找到val_acc的峰值点并标记
        val_acc_peak_index = np.argmax(self.val_acc_lst)
        plt.scatter(val_acc_peak_index, self.val_acc_lst[val_acc_peak_index], color="blue", marker="v", s=100)
        plt.xlabel("epoch")
        plt.ylabel("acc")
        plt.ylim(-0.05, 1.05)
        plt.legend(loc='lower right')

        if self.isBinaryCls:
            plt.subplot(3, 1, 3)
            plt.plot(self.val_f1_lst, color=palette[0], label="f1")
            plt.plot(self.val_L0_True_lst, color=palette[1], label="L0_True")
            plt.plot(self.val_L1_True_lst, color=palette[2], label="L1_True")

            # 找到val_f1的峰值点并标记
            val_f1_peak_index = np.argmax(self.val_f1_lst)
            plt.scatter(val_f1_peak_index, self.val_f1_lst[val_f1_peak_index], color=palette[0], marker="v", s=100)

            # 找到val_L0_True的峰值点并标记
            val_L0_True_peak_index = np.argmax(self.val_L0_True_lst)
            plt.scatter(val_L0_True_peak_index, self.val_L0_True_lst[val_L0_True_peak_index], color=palette[1],
                        marker="v", s=100)

            # 找到val_L1_True的峰值点并标记
            val_L1_True_peak_index = np.argmax(self.val_L1_True_lst)
            plt.scatter(val_L1_True_peak_index, self.val_L1_True_lst[val_L1_True_peak_index], color=palette[2],
                        marker="v", s=100)

            plt.xlabel("epoch")
            plt.ylabel("score")
            plt.ylim(-0.05, 1.05)
            plt.legend(loc='lower right')

        plt.savefig(jpg_path)
        print(f"[draw] picture 已保存到{jpg_path}")
        if if_show:
            plt.show()
        plt.close()

    def _print_and_toWriter(self, info: str, if_print=True):
        if if_print:
            print(info)
        if self.writer is not None:
            self.writer.toFile(info)
    def _train_once(self, epoch, epochs, inputs_func, outputs_func, labels_func):
        bar = BTqdm(total=len(self.train_loader))
        current_lr = self.optimizer.param_groups[0]['lr']

        self.model.train()
        correct = 0
        total = 0
        losses = 0
        for iter, (inputs, labels) in enumerate(self.train_loader):
            # 基本训练
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            labels = labels_func(labels)
            inputs = inputs_func(inputs)
            outputs = self.model(inputs)
            outputs = outputs_func(outputs)

            loss = self.criterion(outputs, labels)
            self.optimizer.zero_grad()  # 清零梯度
            loss.backward()  # 计算梯度
            self.optimizer.step()  # 更新参数
            # SNN
            if self.isSpikingjelly:
                from spikingjelly.activation_based import functional
                functional.reset_net(self.model)
            # 进度条
            bar.update(
                1,
                setting=BColor.BLUE+BAppearance.HIGHLIGHT,
                prefix=f"{BColor.BLUE}Epoch [{epoch}/{epochs}]",
                suffix=f"lr: {current_lr:.2e}, loss: {loss.item():.3f}"
            )
            # 数据记录
            self.train_loss_lst.append(loss.item())
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            losses += loss.item()
        accuracy = correct / total
        train_loss = losses / len(self.train_loader)
        print(f'Epoch [{epoch}/{epochs}], train_loss: {train_loss:.3f}, train_Acc: {accuracy:.3f}', end='')
        self.train_acc_lst.append(accuracy)
        # 更新学习率
        if self.lrScheduler:
            self.lrScheduler.step()

        return accuracy, train_loss, current_lr

    def _eval_once(self, inputs_func, outputs_func, labels_func):
        self.model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                labels = labels_func(labels)
                inputs = inputs_func(inputs)
                outputs = self.model(inputs)
                outputs = outputs_func(outputs)
                _, predicted = torch.max(outputs, 1)

                if self.isSpikingjelly:
                    from spikingjelly.activation_based import functional
                    functional.reset_net(self.model)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())

            # 记录accuracy
            accuracy = correct / total
            print(f', val_Acc: {accuracy:.3f}')
            self.val_acc_lst.append(accuracy)

            # 保存最优模型
            if accuracy > self._best_acc:
                self._best_acc = accuracy
                self._best_model_state_dict = copy.deepcopy(self.model.state_dict())
                self._best_optimizer_state_dict = copy.deepcopy(self.optimizer.state_dict())
                self._best_lrScheduler_state_dict = copy.deepcopy(self.lrScheduler.state_dict()) if self.lrScheduler else None

            if self.isBinaryCls:
                cm = self._get_confusion_matrix(y_true, y_pred)
                TN = cm[0, 0]
                FP = cm[0, 1]
                FN = cm[1, 0]
                TP = cm[1, 1]

                f1 = self._get_f1_score(y_true, y_pred)
                self.val_f1_lst.append(f1)

                L0_True = self._get_L0_True(TN, FP)
                self.val_L0_True_lst.append(L0_True)

                L1_True = self._get_L1_True(FN, TP)
                self.val_L1_True_lst.append(L1_True)

        return accuracy

    def _get_confusion_matrix(self, y_true, y_pred):
        from sklearn.metrics import confusion_matrix
        result = confusion_matrix(y_true, y_pred)
        return result
    def _get_f1_score(self, y_true, y_pred):
        from sklearn.metrics import f1_score
        result = f1_score(y_true, y_pred, average='macro')
        return result
    def _get_recall(self, y_true, y_pred):
        from sklearn.metrics import recall_score
        result = recall_score(y_true, y_pred, average='macro')
        return result
    def _get_precision(self, y_true, y_pred):
        from sklearn.metrics import precision_score
        result = precision_score(y_true, y_pred, average='macro')
        return result

    def _get_L0_True(self, TN, FP):
        return TN / (TN + FP)

    def _get_L1_True(self, FN, TP):
        return TP / (TP + FN)