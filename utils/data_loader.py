import tensorflow as tf
import numpy as np

def load_emotion_data(data_dir='data/emotion',img_size=(224,224),batch_size=32):
    """
    加载emotion数据集
    :param data_dir:数据根目录
    :param img_size:统一后的图片大小
    :param batch_size:批次
    :return:TF Dataset对象（images，labels）
    """
    return tf.keras.preprocessing.image_dataset_from_directory(
        directory=data_dir,
        labels='inferred',      # 从子目录自动获取标签
        label_model='int',      # 表情转为0-6的整数
        color_mode='rgb',
        batch_size=batch_size,
        image_size=img_size,
        shuffle=True,
        seed=42,
        validation_split=0.2,   # 自动划分验证集
        subset='both'           # 返回（train_ds,val_ds）
    )