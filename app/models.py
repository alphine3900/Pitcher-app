from flask_login import UserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.String)
    pitch = db.Column(db.String(255))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    upvote = db.relationship('Upvote',backref='new',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='new',lazy='dynamic')
    comment = db.relationship('Comment',backref='new',lazy='dynamic')


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255),index=True)
    email=db.Column(db.String(255),index=True)
    biography=db.Column(db.String(255))
    profile_pic=db.Column(db.String())
    password_secure=db.Column(db.String(255))
    pitches= db.relationship('Pitch',backref = 'user',lazy ="dynamic")
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')
    comment = db.relationship('Comment',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_secure, password)

    def __repr__(self):
        return f'User: {self.username}'

@login_manager.user_loader
def load_user(user_id):
    """call back function that retrieves a user when a unique identifier is passed"""
    return User.query.get(int(user_id))

def __repr__(self):
    return f'User: {self.name}'


class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote_results = Upvote.query.filter_by(pitch_id=id).all()
        return upvote_results

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'


class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote_results = Downvote.query.filter_by(pitch_id=id).all()
        return downvote_results

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments_results = Comment.query.filter_by(pitch_id=pitch_id).all()

        return comments_results

    def __repr__(self):
        return f'comment:{self.comment}'


