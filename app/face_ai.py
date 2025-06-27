# 该文件对外提供图片分类，打分方法
import os

from flask import jsonify

from models.predict_scripts.emotion_predict import EmotionPredictor
from models.predict_scripts.score_predict import get_model,get_score

"""SCORE_MODEL_DIR="D:\\UserResource\\Code\\CharmPk\\models\\score_model.pth"
EMOTION_MODEL_DIR="D:\\UserResource\\Code\\CharmPk\\models\\emotion_model.pth" """

SCORE_MODEL_DIR="models\\score_model.pth"
EMOTION_MODEL_DIR="models\\emotion_model.pth"

score_model=get_model()

emotion_predict=EmotionPredictor(EMOTION_MODEL_DIR)

def get_emotion(img_path):
    result=emotion_predict.predict_image(img_path)
    return result['predicted_class']
def get_result(img_path):
    score=str(get_score(score_model,img_path))
    emotion=get_emotion(img_path)
    return {"score":score,"emotion":emotion}
