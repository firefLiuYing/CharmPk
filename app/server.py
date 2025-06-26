# app/server.py
from flask import Flask,request
from app.models import db
from app import app
from app.database import print_all_tablename

with app.app_context():
    db.create_all()
    print_all_tablename()

@app.route('/hello',methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/register',methods=['POST'])
def register():
    data=request.json
    user_name=data.get('username')
    password=data.get('password')

