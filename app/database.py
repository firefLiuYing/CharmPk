from app import db
from app.models import User, Photo, Friend, Post, Comment, Like, PkResult
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# 创建用户
def create_user(username, password, email=None):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# 获取用户通过用户名
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

# 获取用户通过uid
def get_user_by_uid(uid):
    return User.query.filter_by(uid=uid).first()

# 创建好友请求
def create_friend_request(uid1, uid2):
    friend_request = Friend(uid1=uid1, uid2=uid2, status='pending')
    db.session.add(friend_request)
    db.session.commit()
    return friend_request

# 接受好友请求
def accept_friend_request(friend_id):
    friend = Friend.query.get(friend_id)
    if friend:
        friend.status = 'accepted'
        db.session.commit()
        return friend
    return None

# 创建帖子
def create_post(uid, content):
    new_post = Post(uid=uid, content=content)
    db.session.add(new_post)
    db.session.commit()
    return new_post

# 创建评论
def create_comment(post_id, uid, content):
    new_comment = Comment(post_id=post_id, uid=uid, content=content)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment

# 点赞操作
def like_post_or_comment(user_id, post_id=None, comment_id=None):
    like = Like(user_id=user_id, post_id=post_id, comment_id=comment_id)
    db.session.add(like)
    db.session.commit()
    return like

# 上传照片
def add_photo(uid, image_url, score):
    new_photo = Photo(uid=uid, image_url=image_url, score=score)
    db.session.add(new_photo)
    db.session.commit()
    return new_photo

# 创建PK对战记录
def create_pk_result(uid1, uid2, winner_uid, score1, score2):
    pk_result = PkResult(uid1=uid1, uid2=uid2, winner_uid=winner_uid, score1=score1, score2=score2)
    db.session.add(pk_result)
    db.session.commit()
    return pk_result
