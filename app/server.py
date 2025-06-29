# app/server.py
import atexit
import shutil
import tempfile
from flask import Flask, request, jsonify,send_from_directory
from app import app
from app.database import *
from app.tools import *
import os
from werkzeug.utils import secure_filename
import random
import time
from app import database
"""from app.face_ai import get_result"""


class Config:
    TEMP_DIR=os.path.join(tempfile.gettempdir(),'image_library_temp')
    STORAGE_MODE='temp'
os.makedirs(Config.TEMP_DIR,exist_ok=True)
app.config['TEMP_DIR']=Config.TEMP_DIR
default_icon_origin_path=os.path.join('user_data/icon/default_icon.png')
default_icon_target_path=os.path.join(app.config['TEMP_DIR'],'default_icon.png')
shutil.copy(default_icon_origin_path,default_icon_target_path)
app.config['DEFAULT_ICON']='default_icon.png'

@atexit.register
def cleanup():
    if Config.STORAGE_MODE=='temp' and os.path.exists(Config.TEMP_DIR):
        shutil.rmtree(Config.TEMP_DIR)
        print(f"已清理临时目录：{Config.TEMP_DIR}")

with app.app_context():
    db.create_all()
    print_all_tablename()

@app.route('/log',methods=['GET'])
def log():
    print_all_table()
    return jsonify({'check_code':520})

@app.route('/faceEvaluate',methods=['POST'])
def face_predict():
    if 'image' not in request.files:
        return jsonify({'check_code':103})
    image=request.files['image']
    if image.filename == '':
        return jsonify({'check_code':104})
    else:
        timestamp=str(int(time.time()*1000))
        filename=timestamp+'_'+secure_filename(image.filename)
        image_path=os.path.join(app.config['TEMP_DIR'],filename)
        image.save(image_path)
        image_url=f'http://127.0.0.1:5000/download/{filename}'
        user_id=request.form.get('user_id')
        random_num=random.random()
        score=60+40*random_num
        score=round(score,2)
        result=upload_photo(user_id, score, image_url=image_url)
        if result['check_code']==520:
            return jsonify({'check_code':520,'point':score})
        return jsonify({'check_code':101,'point':score})

@app.route('/download/<filename>',methods=['GET'])
def download(filename):
    if os.path.exists(os.path.join(app.config['TEMP_DIR'],filename)):
        return send_from_directory(app.config['TEMP_DIR'],filename)
    return jsonify({'error':'File Not Found'}),404

@app.route('/login',methods=['POST'])
def login():
    username=request.get_json().get('username')
    password=request.get_json().get('password')
    result=login_user(username, password)
    if result['check_code']==101:
        return jsonify(result)
    user_icon=result['user_icon']
    nickname=result['nickname']
    user_id=result['user_id']
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':nickname,'user_id':user_id})

@app.route('/register',methods=['POST'])
def register():
    username=request.get_json().get('username')
    password=request.get_json().get('password')
    result=register_user(username, password)
    if result['check_code']==102:
        return jsonify({'check_code':102})
    user_icon = 'http://127.0.0.1:5000/download/default_icon.png'
    user_id=result['user_id']
    return jsonify({'check_code':520,'user_icon':user_icon,'nickname':result['nickname'],'user_id':user_id})

@app.route('/loadUserCharmRanking',methods=['POST'])
def load_user_charm_ranking():
    user_id=request.get_json().get('user_id')
    result=get_photos(user_id)
    return jsonify({'check_code':520,'images':result['images'],'points':result['points']})

@app.route('/searchUser',methods=['POST'])
def search_user():
    nickname=request.get_json().get('nickname')
    result=database.search_user(nickname)
    return jsonify(result)

@app.route('/applyForFriends',methods=['POST'])
def apply_friend():
    user_id_1=request.get_json().get('user_id_1')
    user_id_2=request.get_json().get('user_id_2')
    result=create_friendship(user_id_1, user_id_2)
    return jsonify(result)

@app.route('/loadApplication',methods=['POST'])
def load_applications():
    user_id=request.get_json().get('user_id')
    result=database.load_applications(user_id)
    return result

@app.route('/acceptApplication',methods=['POST'])
def accept_application():
    user_id_1=request.get_json().get('user_id_1')
    user_id_2=request.get_json().get('user_id_2')
    result =accept_friend_apply(user_id_1, user_id_2)
    return jsonify(result)

@app.route('/refuseApplication',methods=['POST'])
def refuse_application():
    user_id_1=request.get_json().get('user_id_1')
    user_id_2=request.get_json().get('user_id_2')
    result=refuse_friend_apply(user_id_1, user_id_2)
    return jsonify(result)

@app.route('/loadFriends',methods=['POST'])
def load_friends():
    user_id=request.get_json().get('user_id')
    result=database.load_friends(user_id)
    return jsonify(result)

@app.route('/loadPkRecords',methods=['POST'])
def load_pk():
    user_icon = process_image('user_data/icon/default_icon.png')
    return jsonify({'check_code':999,'user_icon_1':user_icon,'nickname_1':'用户0d00','user_icon_2':user_icon,'nickname_2':'用户0721'})

@app.route('/createPkRecords',methods=['POST'])
def create_pk():
    user_id_1=request.get_json().get('user_id_1')
    user_id_2=request.get_json().get('user_id_2')
    result=database.create_pk(user_id_1, user_id_2)
    return jsonify(result)

@app.route('/loadPkApplication',methods=['POST'])
def load_pk_application():
    user_id=request.get_json().get('user_id')
    result=database.load_pk_application(user_id)
    return jsonify(result)

@app.route('/acceptPkApplication',methods=['POST'])
def accept_pk_application():
    pk_id=request.get_json().get('pk_id')
    result=accept_pk(pk_id)
    return jsonify(result)

@app.route('/refusePkApplication',methods=['POST'])
def refuse_pk_application():
    pk_id=request.get_json().get('pk_id')
    result=refuse_pk(pk_id)
    return jsonify(result)

@app.route('/loadCurrentPk',methods=['POST'])
def load_current_pk():
    user_id=request.get_json().get('user_id')
    result=database.load_current_pk(user_id)
    return result

@app.route('/createNews',methods=['POST'])
def create_post():
    return jsonify({'check_code': 520})

