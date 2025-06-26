# app/server.py
from flask import Flask, request, jsonify
from app.models import db
from app import app
import base64
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

@app.route('/login',methods=['POST'])
def login():
    return jsonify({'check_code':999,'nickname':'用户0721'})

@app.route('/register',methods=['POST'])
def register():
    return jsonify({'check_code':999,'nickname':'用户0721'})

@app.route('/loadUserCharmRanking',methods=['POST'])
def load_user_charm_ranking():
    return jsonify({'check_code':999,'images':[],'points':[]})

@app.route('/searchUser',methods=['POST'])
def search_user():
    return jsonify({'check_point':999,'nickname':'用户0d00'})

@app.route('/applyForFriends',methods=['POST'])
def apply_friend():
    return jsonify({'check_code':999,'nickname':'用户0d000721'})

@app.route('/acceptApplication',methods=['POST'])
def accept_application():
    return jsonify({'check_code':520})

@app.route('/refuseApplication',methods=['POST'])
def refuse_application():
    return jsonify({'check_code':520})

@app.route('/loadFriends',methods=['POST'])
def load_friends():
    return jsonify({'check_code':520,'user_icons':[],'nicknames':[],'usernames':[]})

@app.route('/loadPkRecords',methods=['POST'])
def load_pk():
    return jsonify({'check_code':999,'nickname_1':'用户0d00','nickname_2':'用户0721'})

@app.route('/createPkRecords',methods=['POST'])
def create_pk():
    return jsonify({'check_code':520})

@app.route('/loadPkApplication',methods=['POST'])
def load_pk_application():
    return jsonify({'check_code':520,'user_icons':[],'nicknames':[],'usernames':[]})

@app.route('/acceptPkApplication',methods=['POST'])
def accept_pk_application():
    return jsonify({'check_code':520})

@app.route('/refusePkApplication',methods=['POST'])
def refuse_pk_application():
    return jsonify({'check_code': 520})

@app.route('/createNews',methods=['POST'])
def create_post():
    return jsonify({'check_code': 520})