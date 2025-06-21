import os
import tempfile
from flask import Flask, request, jsonify
from models.predict_scripts.score_predict import get_model, get_score

app = Flask(__name__)
pipeline = get_model()

@app.route('/upload', methods=['POST'])
def upload():
    # 获取图片文件
    photo = request.files['photo']
    user_id = request.form['user_id']

    # 将图片保存到临时文件夹
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    photo.save(temp_file.name)
    # 获取分数
    try:
        img_path=temp_file.name
        score = get_score(pipeline,img_path)
    finally:
        temp_file.close()
        os.remove(temp_file.name)
    return jsonify({"score": score})


if __name__ == '__main__':
    app.run(debug=False)
