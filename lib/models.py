import os
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import false
from . import db
from sqlalchemy.sql import func


SECRET_KEY = os.environ.get("KEY")



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150),unique = True)
    user_name = db.Column(db.String(150),unique = True)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    password = db.Column(db.String(150))
    notes = db.relationship('Note', backref='author', lazy=True)

    
    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET_KEY, expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    
# class Upload(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(50))
#     data = db.Column(db.LargeBinary)
    
#     def __init__(self, filename, data):
#         self.filename = filename
#         self.data = data


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))