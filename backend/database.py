# 该文件对外提供数据库相关方法
from flask import jsonify

def write_user(user_info):
    user_id=0
    return user_id
def read_user(user_id):
    user_info=jsonify({"id":user_id})
    return user_info
def write_post(post_info):
    post_id=0
    return post_id
def read_post(post_id):
    post_info=jsonify({"id":post_id})
    return post_info
def write_image(image_info):
    image_id=0
    return image_id
def read_image(image_id):
    image_info=jsonify({"id":image_id})
    return image_info
def write_comment(comment_info):
    comment_id=0
    return comment_id
def read_comment(comment_id):
    comment_info=jsonify({"id":comment_id})
    return comment_info