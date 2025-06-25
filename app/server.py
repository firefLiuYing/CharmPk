# app/server.py
from flask import Flask,request
from app.database import db
from app import app
from sqlalchemy import inspect

with app.app_context():
    db.create_all()
    inspector=inspect(db.engine)
    tables=inspector.get_table_names()
    print("数据库中的表有：",tables)

@app.route('/hello',methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/register',methods=['POST'])
def register():
    data=request.json
    user_name=data.get('username')
    password=data.get('password')

