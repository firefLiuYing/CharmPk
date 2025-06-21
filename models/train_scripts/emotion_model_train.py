import os
import torch
import torch.nn as nn
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
from torch.optim import Adam, lr_scheduler
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import argparse

DATA_DIR="D:\\UserResource\\Code\\CharmPk\\model_train_data\\emotion"
BATCH_SIZE=20
EPOCHS=32
LR=0.001
NUM_WORKERS=4
OUTPUT_DIR="D:\\UserResource\\Code\\CharmPk\\models"

# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# 数据增强和变换
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# 加载数据集
def load_datasets(data_dir):
    train_dir = os.path.join(data_dir, 'train')
    test_dir = os.path.join(data_dir, 'test')

    train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
    test_dataset = datasets.ImageFolder(test_dir, transform=test_transform)

    return train_dataset, test_dataset


# 修正后的模型定义
class EmotionClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # 使用最新torchvision API加载预训练模型
        self.base_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        # 冻结所有卷积层
        for param in self.base_model.parameters():
            param.requires_grad = False

        # 替换最后的全连接层
        num_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        # 直接使用完整的base_model，不要单独调用fc
        return self.base_model(x)

    def unfreeze_layers(self, num_layers=3):
        """解冻顶层进行微调"""
        children = list(self.base_model.children())
        for child in children[-num_layers:]:
            for param in child.parameters():
                param.requires_grad = True


# 训练函数
def train_model(model, train_loader, test_loader, criterion, optimizer, scheduler, epochs, device, output_dir):
    best_acc = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        running_correct = 0
        total = 0

        pbar = tqdm(train_loader, desc=f'Train Epoch {epoch + 1}/{epochs}')
        for inputs, labels in pbar:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_correct += torch.sum(preds == labels.data)
            total += labels.size(0)

            pbar.set_postfix({
                'loss': running_loss / total,
                'acc': running_correct.double() / total
            })

        train_loss = running_loss / len(train_loader.dataset)
        train_acc = running_correct.double() / len(train_loader.dataset)
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)

        # 验证阶段
        val_loss, val_acc = validate(model, test_loader, criterion, device)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        scheduler.step()

        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'class_names': train_loader.dataset.classes
            }, os.path.join(output_dir, 'emotion_model.pth'))

        print(f'Epoch {epoch + 1}/{epochs}: '
              f'Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | '
              f'Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}')

    # 绘制训练曲线
    plot_training_history(history, output_dir)

    return model


def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_correct = 0

    with torch.no_grad():
        for inputs, labels in tqdm(loader, desc='Validating'):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_correct += torch.sum(preds == labels.data)

    loss = running_loss / len(loader.dataset)
    acc = running_correct.double() / len(loader.dataset)

    return loss, acc


def plot_training_history(history, output_dir):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot([x.cpu() for x in history['train_loss']], label='Train Loss')
    plt.plot([x.cpu() for x in history['val_loss']], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot([x.cpu() for x in history['train_acc']], label='Train Accuracy')
    plt.plot([x.cpu() for x in history['val_acc']], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.savefig(os.path.join(output_dir, 'training_history.png'))
    plt.close()

def main():
    # 加载数据集
    train_dataset, test_dataset = load_datasets(DATA_DIR)
    class_names = train_dataset.classes
    num_classes = len(class_names)
    print(f"发现 {num_classes} 个表情类别: {class_names}")

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    # 初始化模型
    model = EmotionClassifier(num_classes).to(device)
    model.unfreeze_layers(3)  # 解冻最后3层

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=LR)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    # 训练模型
    print("开始训练...")
    train_model(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        epochs=EPOCHS,
        device=device,
        output_dir=OUTPUT_DIR
    )

    print("训练完成！最佳模型已保存到:", os.path.join(OUTPUT_DIR, 'emotion_model.pth'))


if __name__ == '__main__':
    main()