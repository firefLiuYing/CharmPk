# 该文件给前端提供接口

from flask import Flask,request,jsonify
from sympy import false

from database import init_database,check_database

app = Flask(__name__)
init_database() # 初始化数据库
check_database() # 检查数据库是否存在（调试用，正式版可删掉）

@app.route('/upload',methods=['POST'])
def upload():
    photo =request.files['photo']
    user_id=request.form['user_id']
    # 待补充
    score=80.0
    return jsonify({"score": score})
if __name__ == '__main__':
    app.run(debug=false)
