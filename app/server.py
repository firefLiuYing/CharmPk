# app/server.py
from flask import Flask, request, jsonify
from app.models import db
from app import app
import base64
from app.database import *
from app.tools import *


with app.app_context():
    db.create_all()
    print_all_tablename()

@app.route('/login',methods=['POST'])
def login():
    user_icon=process_image('user_data/icon/default_icon.png')
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':'用户0721'})

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    result=create_user(username,password)
    if result['check_code']==102:
        return jsonify({'check_code':102})
    user_icon = process_image('user_data/icon/default_icon.png')
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':result['nickname']})

@app.route('/loadUserCharmRanking',methods=['POST'])
def load_user_charm_ranking():
    return jsonify({'check_code':520,'images':[],'points':[]})

@app.route('/searchUser',methods=['POST'])
def search_user():
    user_icon = process_image('user_data/icon/default_icon.png')
    return jsonify({'check_point':520,'user_icon':user_icon,'nickname':'用户0d00'})

@app.route('/applyForFriends',methods=['POST'])
def apply_friend():
    user_icon = process_image('user_data/icon/default_icon.png')
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':'用户0d000721'})

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
    user_icon = process_image('user_data/icon/default_icon.png')
    return jsonify({'check_code':999,'user_icon_1':user_icon,'nickname_1':'用户0d00','user_icon_2':user_icon,'nickname_2':'用户0721'})

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