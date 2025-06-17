# 该文件对外提供数据库相关方法
from flask import jsonify
import sqlite3
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
DB_PATH = Path(__file__).parent / "charm_pk.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    conn=get_db_connection()
    cursor=conn.cursor()

    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 用户ID
        name TEXT NOT NULL UNIQUE,              -- 用户唯一标识（用户名）
        secret_key TEXT NOT NULL,               -- 用户密码
        posts TEXT,                             -- 用户发布的帖子ID列表
        images TEXT,                            -- 用户上传的图片ID列表
        comments TEXT,                          -- 用户上传的评论ID列表
        friends TEXT                            -- 用户的好友ID列表
    );
    ''')

    # 创建帖子表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS post(
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 帖子ID
        title TEXT NOT NULL,                    -- 帖子标题
        content TEXT,                           -- 帖子内容
        poster INTEGER,                         -- 发布者ID
        comments TEXT,                          -- 评论ID列表
        thumbs INTEGER DEFAULT 0                -- 点赞数
    );
    ''')

    # 创建图片表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS image(
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 图片ID
        model_train_data BLOB,                              -- 图片数据
        score INTEGER,                          -- 图片颜值
        sex TEXT,                               -- 性别
        age TEXT,                               -- 年龄段
        emoji TEXT,                             -- 表情
        face_shape TEXT                         -- 脸型
    );
    ''')

    # 创建评论表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 评论ID
        commenter INTEGER,                      -- 评论发布者ID
        content TEXT,                           -- 评论内容
        thumbs INTEGER DEFAULT 0                -- 评论点赞数
    );
    ''')

    # 创建Pk记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pk_record(
        id ,
        user_a_id ,
        user_b_id ,
    );
    ''')

    # 提交操作并关闭连接
    conn.commit()
    conn.close()
    return

def check_database():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("SElECT name FROM sqlite_master WHERE type='table';")
    tables=[table[0] for table in cursor.fetchall()]
    conn.close()
    logging.info("数据库中的表：%s",tables)
    return

