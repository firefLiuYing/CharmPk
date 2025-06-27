# app/server.py
import atexit
import shutil
import tempfile
from flask import Flask, request, jsonify
from app import app
from app.database import *
from app.tools import *
import os
"""from app.face_ai import get_result"""


class Config:
    TEMP_DIR=os.path.join(tempfile.gettempdir(),'image_library_temp')
    STORAGE_MODE='temp'
os.makedirs(Config.TEMP_DIR,exist_ok=True)
@atexit.register
def cleanup():
    if Config.STORAGE_MODE=='temp' and os.path.exists(Config.TEMP_DIR):
        shutil.rmtree(Config.TEMP_DIR)
        print(f"已清理临时目录：{Config.TEMP_DIR}")

def save_uploaded_file(file_stream,filename):
    file_ext=os.path.splitext(filename)[1] or '.jpg'
    safe_filename=f"{os.urandom(8).hex()}{file_ext}"
    save_path=os.path.join(Config.TEMP_DIR,safe_filename)
    try:
        img=Image.open(file_stream)
        img.verify()
        file_stream.seek(0)
        with open(save_path,'wb') as f:
            f.write(file_stream.read())
        return save_path
    except Exception as e:
        print(f"文件保存失败：{str(e)}")
        if os.path.exists(save_path):
            os.remove(save_path)
        raise

with app.app_context():
    db.create_all()
    print_all_tablename()

@app.route('/faceEvaluate',methods=['POST'])
def face_predict():
    """if 'username' not in request.form:
        return jsonify({'check_code':103})

    if 'image' not in request.files:
        return jsonify({'check_code':103})
    file=request.files['image']
    if file.filename=='':
        return jsonify({'check_code':104})
    img_path=save_uploaded_file(file.stream,file.filename)
    calculate_result=get_result(img_path)"""
    return jsonify({'check_code':520})


@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    result=login_user(username, password)
    if result['check_code']==101:
        return jsonify(result)
    user_icon=process_image(result['user_icon'])
    nickname=result['nickname']
    user_id=result['id']
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':nickname,'user_id':user_id})

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    result=register_user(username, password)
    if result['check_code']==102:
        return jsonify({'check_code':102})
    user_icon = process_image('user_data/icon/default_icon.png')
    user_id=result['user_id']
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':result['nickname'],'user_id':user_id})

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

