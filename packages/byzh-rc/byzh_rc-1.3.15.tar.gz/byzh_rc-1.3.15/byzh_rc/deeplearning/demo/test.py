import torch
from torch import nn

from ..trainers import BTrainer
from ..utils import get_device

class testNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer0 = nn.Sequential(
            nn.Linear(1*28*28, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.layer0(x)
        return x

def get_dataloader(batch_size):
    from torch.utils.data import TensorDataset
    from torch.utils.data import random_split, DataLoader
    # 随机生成数据张量和标签张量
    data = torch.randn(6000, 1, 28, 28)
    labels = torch.randint(0, 10, (6000,)) # 标签为0~9, shape=(6000,)
    # 创建TensorDataset对象
    datasets = TensorDataset(data, labels)
    # 随机划分训练集和验证集
    train_datasets, val_datasets = random_split(datasets, [5500, 500])
    # 创建DataLoader对象
    train_dataloader = DataLoader(train_datasets, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_datasets, batch_size=8, shuffle=False)
    return train_dataloader, val_dataloader

def Btest():
    print(f"{'='*10} test.py start {'='*10}")

    #### 超参数 ####
    lr = 1e-4
    batch_size = 64
    epochs = 5
    device = get_device(sout=True)

    #### 数据集 ####
    train_dataloader, val_dataloader = get_dataloader(batch_size)
    print(f"{'='*10} TensorDataset 创建完成 {'='*10}")

    #### 模型 ####
    net = testNet()
    net.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    #### Trainer ####
    myTrainer = BTrainer(net, train_dataloader, val_dataloader, optimizer, criterion, device,
                         isParallel=True)
    #### 训练 ####
    myTrainer.train_eval_s(epochs)
    print(f"{'='*10} test.py success {'='*10}")

if __name__ == '__main__':
    Btest()