# 该文件给前端提供接口

from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/upload',methods=['POST'])
def upload():
    photo =request.files['photo']
    user_id=request.form['user_id']
    # 待补充
    score=80.0
    return jsonify({"score": score})
if __name__ == '__main__':
    app.run(debug=True)
