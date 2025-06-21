# app/server.py
from flask import Flask
from app.database import db

# 创建 Flask 应用对象
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # 初始化数据库

# 定义一些路由（视图函数）
@app.route('/hello',methods=['GET'])
def home():
    return 'Hello, World!'
