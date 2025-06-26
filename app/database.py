from app.models import User,db
from sqlalchemy import inspect

def commit_all():
    """推送所有更改,每次推送完一批更改后一定要记得推送，
    最好是更改一批然后再推送而非改一点推送一点"""
    db.session.commit()
    return

def print_all_tablename():
    inspector=inspect(db.engine)
    tables=inspector.get_table_names()
    print("所有表的名字："+tables)

def create_user(username,nickname,password_hash):
    new_user=User(username=username,nickname=nickname,password_hash=password_hash)
    db.session.add(new_user)

