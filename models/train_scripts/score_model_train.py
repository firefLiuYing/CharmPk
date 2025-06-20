import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.tensorboard import SummaryWriter
import torchvision.transforms as transforms
from torchvision.models import efficientnet_v2_s
from torchvision.transforms import autoaugment

# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
IMG_DIR="D:\\UserResource\\Code\\CharmPk\\model_train_data\\score\\Images\\Images"
RATING_PATH="D:\\UserResource\\Code\\CharmPk\\model_train_data\\score\\labels.txt"


# 早停机制
class EarlyStopping:
    def __init__(self, patience=5, delta=0):
        self.patience = patience
        self.delta = delta
        self.counter = 0
        self.best_score = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_score is None:
            self.best_score = val_loss
        elif val_loss > self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = val_loss
            self.counter = 0


# 数据集类
class BeautyDataset(Dataset):
    def __init__(self, img_dir, df, transform=None):
        self.img_dir = img_dir
        self.df = df
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.df.iloc[idx]['filename'])
        try:
            image = Image.open(img_path).convert('RGB')
            rating = self.df.iloc[idx]['rating']
            normalized_rating = (rating - 1) / 4.0

            if self.transform:
                image = self.transform(image)

            return image, torch.tensor(normalized_rating, dtype=torch.float32)
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            # 返回一个空图像和平均评分作为占位符
            dummy_img = torch.zeros(3, 224, 224)
            return dummy_img, torch.tensor(0.5, dtype=torch.float32)


# 模型类
class AdvancedBeautyModel(nn.Module):
    def __init__(self, pretrained=True):
        super().__init__()
        self.backbone = efficientnet_v2_s(weights='DEFAULT' if pretrained else None)
        num_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(num_features, 256),
            nn.SiLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )
        self._unfreeze_layers(5)

    def _unfreeze_layers(self, num_layers):
        children = list(self.backbone.children())
        for child in children[-num_layers:]:
            for param in child.parameters():
                param.requires_grad = True

    def forward(self, x):
        return self.backbone(x)


# 创建数据加载器
def create_data_loaders(img_dir, rating_path, batch_size=32):
    # 加载评分数据
    ratings_df = pd.read_csv(rating_path, sep=' ', header=None, names=['filename', 'rating'])

    # 定义变换
    train_transform = transforms.Compose([
        transforms.Resize(256),
        autoaugment.TrivialAugmentWide(),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 创建完整数据集
    full_dataset = BeautyDataset(img_dir, ratings_df)

    # 划分训练集和验证集
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    # 应用不同的变换
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform

    # Windows上设置num_workers=0以避免多进程问题
    num_workers = 0 if os.name == 'nt' else 4

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False
    )

    return train_loader, val_loader


# 验证函数
def validate(model, loader, criterion, epoch, writer):
    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, ratings in tqdm(loader, desc='Validating'):
            images = images.to(device)
            ratings = ratings.to(device).unsqueeze(1)

            outputs = model(images)
            loss = criterion(outputs, ratings)

            running_loss += loss.item() * images.size(0)
            all_preds.extend(outputs.squeeze().cpu().numpy())
            all_labels.extend(ratings.squeeze().cpu().numpy())

    epoch_loss = running_loss / len(loader.dataset)
    writer.add_scalar('Loss/val', epoch_loss, epoch)

    # 计算评估指标
    all_preds = np.array(all_preds) * 4 + 1  # 转换回1-5分
    all_labels = np.array(all_labels) * 4 + 1

    mae = np.mean(np.abs(all_preds - all_labels))
    pearson = np.corrcoef(all_preds, all_labels)[0, 1]

    writer.add_scalar('Metrics/MAE', mae, epoch)
    writer.add_scalar('Metrics/Pearson', pearson, epoch)

    print(f'\nValidation - Loss: {epoch_loss:.4f}, MAE: {mae:.3f}, Pearson: {pearson:.3f}')
    return epoch_loss


# 主函数
def main():
    # 初始化数据加载器
    train_loader, val_loader = create_data_loaders(
        img_dir=IMG_DIR,  # 替换为你的实际路径
        rating_path=RATING_PATH,  # 替换为你的实际路径
        batch_size=32
    )

    # 初始化模型
    model = AdvancedBeautyModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
    scheduler = CosineAnnealingLR(optimizer, T_max=20, eta_min=1e-6)
    writer = SummaryWriter('runs/beauty_scoring')

    # 训练参数
    best_loss = float('inf')
    early_stopping = EarlyStopping(patience=7)

    # 训练循环
    for epoch in range(50):
        # 训练阶段
        model.train()
        train_loss = 0.0
        for images, ratings in tqdm(train_loader, desc=f'Train Epoch {epoch + 1}'):
            images = images.to(device)
            ratings = ratings.to(device).unsqueeze(1)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, ratings)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)

        train_loss /= len(train_loader.dataset)
        writer.add_scalar('Loss/train', train_loss, epoch)

        # 验证阶段
        val_loss = validate(model, val_loader, criterion, epoch, writer)
        scheduler.step()

        # 保存最佳模型
        if val_loss < best_loss:
            best_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': val_loss,
            }, 'best_model.pth')

        # 早停检查
        early_stopping(val_loss)
        if early_stopping.early_stop:
            print(f"Early stopping at epoch {epoch + 1}")
            break

    writer.close()
    print("Training completed!")


if __name__ == '__main__':
    # Windows多进程支持
    torch.multiprocessing.freeze_support()

    # 运行主函数
    main()