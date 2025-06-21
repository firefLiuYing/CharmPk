import os
import torch
from torchvision import transforms
from PIL import Image
import argparse
import torchvision

# 预测用的图像变换
predict_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


class EmotionPredictor:
    def __init__(self, model_path, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = torch.device(device)
        self.load_model(model_path)

    def load_model(self, model_path):
        """加载训练好的模型"""
        checkpoint = torch.load(model_path, map_location=self.device)
        self.class_names = checkpoint['class_names']

        # 初始化模型结构
        self.model = EmotionClassifier(len(self.class_names))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()

    def predict_image(self, image_path):
        """预测单张图片"""
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = predict_transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensor)
                _, preds = torch.max(outputs, 1)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0] * 100

            pred_class = self.class_names[preds.item()]
            confidence = probabilities[preds.item()].item()

            # 获取所有类别的概率
            all_probs = {self.class_names[i]: round(prob.item(), 2)
                         for i, prob in enumerate(probabilities)}

            return {
                'predicted_class': pred_class,
                'confidence': round(confidence, 2),
                'all_probabilities': all_probs,
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def predict_batch(self, folder_path):
        """批量预测文件夹中的图片"""
        results = {}
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(valid_extensions):
                image_path = os.path.join(folder_path, filename)
                results[filename] = self.predict_image(image_path)

        return results


# 需要复制原始模型定义中的EmotionClassifier类
class EmotionClassifier(torch.nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.base_model = torchvision.models.resnet18(pretrained=False)

        # 冻结所有卷积层
        for param in self.base_model.parameters():
            param.requires_grad = False

        # 替换最后的全连接层
        num_features = self.base_model.fc.in_features
        self.base_model.fc = torch.nn.Sequential(
            torch.nn.Linear(num_features, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.base_model(x)

MODEL_DIR="D:\\UserResource\\Code\\CharmPk\\models\\emotion_model.pth"

def main():

    predictor = EmotionPredictor(MODEL_DIR)
    image_path = input("请输入图像路径: ").strip('"')
    # 判断输入是文件还是文件夹
    if os.path.isfile(image_path):
        # 单张图片预测
        result = predictor.predict_image(image_path)

        if result['status'] == 'success':
            print("\n预测结果:")
            print(f"图片: {os.path.basename(image_path)}")
            print(f"预测表情: {result['predicted_class']}")
            print(f"置信度: {result['confidence']}%")
            print("\n所有类别概率:")
            for cls, prob in result['all_probabilities'].items():
                print(f"{cls}: {prob}%")
        else:
            print(f"预测失败: {result['message']}")
    else:
        print(f"错误: 输入路径 {image_path} 不存在")
