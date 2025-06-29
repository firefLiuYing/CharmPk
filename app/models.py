from sqlalchemy.orm import backref

from app import db

# 用户模型
class User(db.Model):
    """自身基本属性"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_icon=db.Column(db.String(255),default='http://127.0.0.1:5000/download/default_icon.png')

    """关联的属性"""
    images=db.relationship('Photo',backref='author',lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments=db.relationship('Comment',backref='author',lazy=True)
    likes=db.relationship('Like',backref='author',lazy=True)
    def __repr__(self):
        return f'<User 昵称：{self.nickname} id：{self.id}>'

# 照片模型
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __repr__(self):
        return f'<Photo {self.id}>'

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    """状态用字符串表示，共三种:
        pending:申请中
        accept:同意
        refuse:拒绝
    """
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_1 = db.relationship('User', foreign_keys=[user_id_1])
    user_2 = db.relationship('User', foreign_keys=[user_id_2])

    def __repr__(self):
        return f'<Friendship {self.user_1.nickname} <-> {self.user_2.nickname} : {self.status}>'

# 帖子模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(63),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post 标题: {self.title} 作者：{self.author.nickname}>'

# 评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<Comment 发布者：{self.author} 内容：{self.content} id：{self.id}>'

# 点赞模型
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Like {self.author.nickname} 赞了 {self.target_type} {self.target_id}>'

# PK对战结果模型
class Pk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'),default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_photo_1=db.Column(db.Integer,db.ForeignKey('photo.id'),nullable=True)
    user_photo_2=db.Column(db.Integer,db.ForeignKey('photo.id'),nullable=True)

    user_1 = db.relationship('User', foreign_keys=[user_id_1])
    user_2 = db.relationship('User', foreign_keys=[user_id_2])
    """共三种状态：
        pending:申请中
        doing:正在pk
        end:比完了
        refuse:拒绝
    """
    status = db.Column(db.String(20), nullable=False, default='pending')

    def __repr__(self):
        return f'<PkResult {self.user_id_1} vs {self.user_id_2}  status: {self.status}>'

