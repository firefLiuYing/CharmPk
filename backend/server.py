import os
import tempfile
from flask import Flask, request, jsonify
from face_ai import get_result

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # 获取图片文件
    photo = request.files['photo']
    user_id = request.form['user_id']

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    photo.save(temp_file.name)
    try:
        img_path=temp_file.name
        result = get_result(img_path)
    finally:
        temp_file.close()
        os.remove(temp_file.name)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False)
