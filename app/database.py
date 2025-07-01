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
    friendship=Friendship.query.filter(((Friendship.user_id_1==user_id_1)&(Friendship.user_id_2==user_id_2))|((Friendship.user_id_1==user_id_2)&(Friendship.user_id_2==user_id_1))).first()
    if friendship:
        if (friendship.status=='pending')|(friendship.status=='accept'):
            return {'check_code':105}
        friendship.status='pending'
        commit_all()
        return {'check_code':520}
    new_friendship=Friendship(user_id_1=user_id_1,user_id_2=user_id_2,status='pending')
    db.session.add(new_friendship)
    commit_all()
    return {'check_code':520}

def accept_friend_apply(user_id_1,user_id_2):
    friendship=Friendship.query.filter_by(user_id_1=user_id_1,user_id_2=user_id_2,status='pending').first()
    if not friendship:
        return {'check_code':106}
    friendship.status='accept'
    commit_all()
    return {'check_code':520,'status':friendship.status}

def refuse_friend_apply(user_id_1,user_id_2):
    friendship=Friendship.query.filter_by(user_id_1=user_id_1,user_id_2=user_id_2,status='pending').first()
    if not friendship:
        return {'check_code':106}
    friendship.status='refuse'
    commit_all()
    return {'check_code':520,'status':friendship.status}

def load_friends(user_id):
    exist_user=User.query.get(user_id)
    if not exist_user:
        return {'check_code':101}
    friends=Friendship.query.filter((Friendship.user_id_1==user_id)&(Friendship.status=='accept'))
    user_icons=[]
    nicknames=[]
    user_ids=[]
    for friend in friends:
        user=User.query.get(friend.user_id_2)
        user_icons.append(user.user_icon)
        nicknames.append(user.nickname)
        user_ids.append(user.id)
    friends=Friendship.query.filter((Friendship.user_id_2==user_id)&(Friendship.status=='accept'))
    for friend in friends:
        user=User.query.get(friend.user_id_1)
        user_icons.append(user.user_icon)
        nicknames.append(user.nickname)
        user_ids.append(user.id)
    return {'check_code':520,'user_icon':user_icons,'user_id':user_ids,'nickname':nicknames}

def load_applications(user_id):
    user=User.query.get(user_id)
    if not user:
        return {'check_code':101}
    friendships=Friendship.query.filter_by(user_id_2=user_id,status='pending').all()
    user_icons=[]
    nicknames=[]
    user_ids=[]
    for friendship in friendships:
        user=User.query.get(friendship.user_id_1)
        user_icons.append(user.user_icon)
        nicknames.append(user.nickname)
        user_ids.append(user.id)
    return {'check_code':520,'user_icon':user_icons,'nickname':nicknames,'user_id':user_ids}

def create_pk(user_id_1,user_id_2):
    has_pk=Pk.query.filter(
        ((Pk.user_id_1==user_id_1)&((Pk.status=='pending')|(Pk.status=='doing')))
        |((Pk.user_id_2==user_id_1)&(Pk.status=='doing'))
    ).all()
    if has_pk:
        return {'check_code':107}
    new_pk=Pk(user_id_1=user_id_1,user_id_2=user_id_2,status='pending')
    db.session.add(new_pk)
    commit_all()
    return {'check_code':520,'pk_id':new_pk.id}

def load_pk_application(user_id):
    pks=Pk.query.filter((Pk.user_id_2==user_id)&(Pk.status=='pending'))
    user_icon=[]
    nickname=[]
    user_id=[]
    pk_id=[]
    for pk in pks:
        user=User.query.get(pk.user_id_1)
        user_icon.append(user.user_icon)
        nickname.append(user.nickname)
        user_id.append(user.id)
        pk_id.append(pk.id)
    return {'check_code':520,'user_icon':user_icon,'nickname':nickname,'user_id':user_id,'pk_id':pk_id}

def load_pk_records(user_id):
    pks=Pk.query.filter(((Pk.user_id_2==user_id)|(Pk.user_id_1==user_id))&(Pk.status=='end'))
    image_1=[]
    nickname_1=[]
    point_1=[]
    image_2=[]
    nickname_2=[]
    point_2=[]
    for pk in pks:
        user_1=User.query.get(pk.user_id_1)
        user_2=User.query.get(pk.user_id_2)
        nickname_1.append(user_1.nickname)
        nickname_2.append(user_2.nickname)
        photo_1=Photo.query.get(pk.user_photo_1)
        photo_2=Photo.query.get(pk.user_photo_2)
        point_1.append(photo_1.score)
        point_2.append(photo_2.score)
        image_1.append(photo_1.image_url)
        image_2.append(photo_2.image_url)
    return {'check_code':520,'image_1':image_1,'image_2':image_2,'point_1':point_1,'point_2':point_2,'nickname_1':nickname_1,'nickname_2':nickname_2}


def accept_pk(pk_id):
    exist_pk=Pk.query.get(pk_id)
    if not exist_pk:
        return {'check_code':108}
    exist_pk.status='doing'
    commit_all()
    return {'check_code':520,'user_id_1':exist_pk.user_id_1,'user_id_2':exist_pk.user_id_2}

def refuse_pk(pk_id):
    exist_pk=Pk.query.get(pk_id)
    if not exist_pk:
        return {'check_code':108}
    exist_pk.status='refuse'
    commit_all()
    return {'check_code':520,'user_id_1':exist_pk.user_id_1,'user_id_2':exist_pk.user_id_2}

def load_current_pk(user_id):
    pk=Pk.query.filter(
        ((Pk.status=='doing')&(Pk.user_id_1==user_id))|
        ((Pk.status=='doing')&(Pk.user_id_2==user_id))|
        ((Pk.status=='pending')&(Pk.user_id_1==user_id))
    ).first()
    if not pk:
        return {'check_code':109}
    user_1=User.query.get(pk.user_id_1)
    user_2=User.query.get(pk.user_id_2)
    if not user_1:
        return {'check_code':101}
    if not user_2:
        return {'check_code':101}
    nickname_1=user_1.nickname
    nickname_2=user_2.nickname
    image_1=None
    image_2=None
    if pk.user_photo_1:
        photo_1=Photo.query.get(pk.user_photo_1)
        image_1=photo_1.image_url
    if pk.user_photo_2:
        photo_2=Photo.query.get(pk.user_photo_2)
        image_2=photo_2.image_url
    return {'check_code':520,'image_1':image_1,'image_2':image_2,'nickname_1':nickname_1,'nickname_2':nickname_2,'pk_id':pk.id}

def upload_image_to_pk(pk_id,user_id,image_url,score):
    exist_pk=Pk.query.get(pk_id)
    if not exist_pk:
        return {'check_code':108}
    new_photo=Photo(user_id=user_id,image_url=image_url,score=score)
    db.session.add(new_photo)
    commit_all()
    photo_id=new_photo.id
    if int(user_id)==int(exist_pk.user_id_1):
        exist_pk.user_photo_1=photo_id
        commit_all()
        return {'check_code':520}
    elif int(user_id)==int(exist_pk.user_id_2):
        exist_pk.user_photo_2=photo_id
        commit_all()
        return {'check_code': 520}
    else:
        print(exist_pk.user_id_1,exist_pk.user_id_2,user_id)
        return {'check_code':110}

def handle_pk(pk_id):
    exist_pk=Pk.query.get(pk_id)
    if not exist_pk:
        return {'check_code':108}
    photo_1=Photo.query.get(exist_pk.user_photo_1)
    if not photo_1:
        return {'check_code':111}
    photo_2=Photo.query.get(exist_pk.user_photo_2)
    if not photo_2:
        return {'check_code':111}
    exist_pk.status='end'
    commit_all()
    return {'check_code':520,'point_1':photo_1.score,'point_2':photo_2.score}

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
