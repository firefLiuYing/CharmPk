from app import db

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    __table_args__={'extend_existing':True}
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'

# 照片模型
class Photo(db.Model):
    __tablename__ = 'photos'
    __table_args__ = {'extend_existing': True}
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('photos', lazy=True))

    def __repr__(self):
        return f'<Photo {self.image_url} with score {self.score}>'

# 好友模型
class Friend(db.Model):
    __tablename__ = 'friends'
    __table_args__ = {'extend_existing': True}
    friend_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid1 = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    uid2 = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='status_enum'), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 帖子模型
class Post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# 评论模型
class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 点赞模型
class Like(db.Model):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# PK对战结果模型
class PkResult(db.Model):
    __tablename__ = 'pk_results'
    __table_args__ = {'extend_existing': True}
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid1 = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    uid2 = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    winner_uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    score1 = db.Column(db.Integer, nullable=False)
    score2 = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
