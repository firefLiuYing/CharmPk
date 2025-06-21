import os
import torch
import torch.nn as nn
from distributed.utils_test import throws
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd

# 解决OpenMP冲突问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class AdvancedBeautyModel(nn.Module):
    def __init__(self, pretrained=True):
        super().__init__()
        from torchvision.models import efficientnet_v2_s
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

    def forward(self, x):
        return self.backbone(x)

class BeautyScoringPipeline:
    def __init__(self, model_path, device='cuda'):
        self.device = device
        self.model = self._load_model(model_path)
        self.transform = self._get_transforms()

    def _load_model(self, model_path):
        model = AdvancedBeautyModel(pretrained=False).to(self.device)

        # 安全加载模型权重
        try:
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=True)
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
        except Exception as e:
            print(f"加载模型失败: {str(e)}")
            raise

        model.eval()
        return model

    def _get_transforms(self):
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            image = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                output = self.model(image)
                score = output.item() * 4 + 1  # 转换回1-5分范围

            return round(score, 2)
        except Exception as e:
            print(f"预测失败: {e}")
            return None

    def predict_and_visualize(self, image_path):
        score = self.predict(image_path)
        if score is None:
            return None

        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(8, 8))
        plt.imshow(image)
        plt.title(f'Predicted Beauty Score: {score:.2f}/5.00', fontsize=14)
        plt.axis('off')

        output_dir = "output_results"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        plt.savefig(output_path, bbox_inches='tight', dpi=100)
        plt.close()

        return score, output_path

def main():
    print("人脸颜值评分系统已加载")
    # 初始化管道
    model_path = "D:\\UserResource\\Code\\CharmPk\\models\\score_model.pth"
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 {model_path} 不存在")
        return

    try:
        pipeline = BeautyScoringPipeline(model_path)
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        return

    while True:
        print("\n1. 单张图像预测")
        print("2. 批量预测目录中的图像")
        print("3. 退出")
        choice = input("请选择操作 (1/2/3): ").strip()

        if choice == '1':
            image_path = input("请输入图像路径: ").strip('"')
            if not os.path.exists(image_path):
                print("文件不存在，请重新输入")
                continue

            result = pipeline.predict_and_visualize(str(image_path))
            if result:
                score, output_path = result
                print(f"预测结果: {score:.2f}/5.00")
                print(f"可视化结果已保存到: {output_path}")

        elif choice == '2':
            image_dir = input("请输入图像目录路径: ").strip('"')
            if not os.path.isdir(image_dir):
                print("目录不存在，请重新输入")
                continue

            results = {}
            for filename in os.listdir(image_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    img_path = os.path.join(image_dir, filename)
                    score = pipeline.predict(img_path)
                    if score is not None:
                        results[filename] = score
                        print(f"{filename}: {score:.2f}/5.00")

            if results:
                output_csv = os.path.join(image_dir, "beauty_scores.csv")
                pd.DataFrame.from_dict(results, orient='index', columns=['Score']).to_csv(output_csv)
                print(f"\n结果已保存到: {output_csv}")
            else:
                print("没有找到有效的图像文件")

        elif choice == '3':
            print("退出系统")
            break

        else:
            print("无效输入，请重新选择")

def initialize():
    torch.multiprocessing.freeze_support()

    # 禁用可能冲突的库的OpenMP
    os.environ['OMP_NUM_THREADS'] = '1'

    # 设置matplotlib后端为非交互式
    plt.switch_backend('Agg')
def get_model():
    initialize()
    model_path = "D:\\UserResource\\Code\\CharmPk\\models\\score_model.pth"
    if not os.path.exists(model_path):
        return f"错误: 模型文件 {model_path} 不存在"
    try:
        pipeline = BeautyScoringPipeline(model_path)
        return pipeline
    except Exception as e:
        return f"初始化失败: {str(e)}"
def get_score(pipeline,img_path):
    if not os.path.exists(img_path):
        return "文件路径不存在"
    result = pipeline.predict(img_path)
    result*=20
    return result
if __name__ == '__main__':
    initialize()
    main()
