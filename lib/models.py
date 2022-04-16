from datetime import timezone
from enum import unique
from sqlalchemy.sql import func
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))

    
    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name

