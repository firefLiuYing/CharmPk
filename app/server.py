# app/server.py
from flask import Flask,request
from app.models import db
from app import app
from app.database import *

with app.app_context():
    db.create_all()
    print_all_tablename()
    create_user('123','龚展鹏',123)
    create_photo(1,100,'qwe')
    create_post(1,'帖子','这是帖子内容')
    create_friendship(1,1)
    create_pk(1,1,1,1,1)
    create_like(1,'post',1)
    create_comment(1,1,'这是评论')
    commit_all()
    print_all_table()

@app.route('/hello',methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/register',methods=['POST'])
def register():
    data=request.json
    user_name=data.get('username')
    password=data.get('password')

