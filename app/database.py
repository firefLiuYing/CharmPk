from app.models import User,Photo,Friendship,Post,Comment,Like,Pk,db
from sqlalchemy import inspect

def commit_all():
    """推送所有更改,每次推送完一批更改后一定要记得推送，
    最好是更改一批然后再推送而非改一点推送一点"""
    db.session.commit()
    return

def print_all_tablename():
    inspector=inspect(db.engine)
    tables=inspector.get_table_names()
    print("所有表的名字：",tables)

def login_user(username,password):
    existing_user=User.query.filter_by(username=username).first()
    if existing_user:
        if existing_user.password_hash==password:
            return {'check_code':520,'nickname':existing_user.nickname,'user_icon':existing_user.user_icon,'user_id':existing_user.id}
        else:
            return {'check_code':101}
    else:
        return {'check_code':101}

def register_user(username, password_hash):
    existing_user=User.query.filter_by(username=username).first()
    if existing_user:
        return {'check_code':102}
    user_count = User.query.count()
    nickname = f"用户{user_count + 1:04d}"
    new_user=User(username=username,nickname=nickname,password_hash=password_hash)
    db.session.add(new_user)
    commit_all()
    return {'check_code':520,'nickname':nickname,'user_id':new_user.id}

def upload_photo(user_id, score, image_url):
    exist_user=User.query.get(user_id)
    if exist_user:
        new_photo=Photo(user_id=user_id,score=score,image_url=image_url)
        db.session.add(new_photo)
        commit_all()
        return {'check_code':520}
    return {'check_code':101}

def get_photos(user_id):
    photos=Photo.query.filter_by(user_id=user_id).order_by(Photo.score.desc()).all()
    scores=[img.score for img in photos]
    urls=[img.image_url for img in photos]
    return {'images':urls,'points':scores}

def search_user(nickname):
    exist_user=User.query.filter_by(nickname=nickname).first()
    if exist_user:
        check_code=520
        user_icon=exist_user.user_icon
        user_id=exist_user.id
        return {'check_code':check_code,'user_icon':user_icon,'user_id':user_id,'nickname':nickname}
    return {'check_code':101}

def create_friendship(user_id_1,user_id_2):
    user=User.query.get(user_id_1)
    if not user:
        return {'check_code':101}
    user=User.query.get(user_id_2)
    if not user:
        return {'check_code':101}
    friendship=Friendship.query.filter((Friendship.user_id_1==user_id_1)&(Friendship.user_id_2==user_id_2)).first()
    if friendship:
        return {'check_code':105}
    friendship=Friendship.query.filter((Friendship.user_id_1==user_id_2)&(Friendship.user_id_2==user_id_1)).first()
    if friendship:
        return {'check_code':106}
    new_friendship=Friendship(user_id_1=user_id_1,user_id_2=user_id_2,status='pending')
    db.session.add(new_friendship)
    commit_all()
    return {'check_code':520}

def create_post(user_id,title,content):
    new_post=Post(user_id=user_id,title=title,content=content)
    db.session.add(new_post)
    return

def create_comment(user_id,post_id,content,comment_id=None):
    new_comment=Comment(user_id=user_id,post_id=post_id,content=content,comment_id=comment_id)
    db.session.add(new_comment)
    return

def create_like(user_id,target_type,target_id):
    new_like=Like(user_id=user_id,target_type=target_type,target_id=target_id)
    db.session.add(new_like)
    return

def create_pk(user_id_1,user_id_2,winner_id,user_photo_1,user_photo_2):
    new_pk=Pk(user_id_1=user_id_1,user_id_2=user_id_2,winner_id=winner_id,user_photo_1=user_photo_1,user_photo_2=user_photo_2)
    db.session.add(new_pk)
    return

def print_all_table():
    users=User.query.all()
    print("User表：")
    for user in users:
        print(user.__repr__())
    photos = Photo.query.all()
    print("Photo表：")
    for photo in photos:
        print(photo.__repr__())
    friendships=Friendship.query.all()
    print("Friendship表：")
    for friendship in friendships:
        print(friendship.__repr__())
    posts=Post.query.all()
    print("Post表：")
    for post in posts:
        print(post.__repr__())
    comments=Comment.query.all()
    print("Comment表：")
    for comment in comments:
        print(comment.__repr__())
    likes=Like.query.all()
    print("Like表：")
    for like in likes:
        print(like.__repr__())
    pks=Pk.query.all()
    print("Pk表：")
    for pk in pks:
        print(pk.__repr__())
