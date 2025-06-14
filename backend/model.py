# 该文件对外提供模型调用相关方法，对内训练模型

import tensorflow as tf
from utils.data_loader import load_emotion_data
import matplotlib.pyplot as plt

def build_emotion_model():
    return