from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import sqlalchemy
from datetime import datetime


db = SQLAlchemy()

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(200))
    edu_login = db.Column(db.String(100))
    edu_password = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    name = db.Column(db.String)
    role = db.Column(db.String)
    class_ = db.Column(db.Integer, db.ForeignKey('class.id'))
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    name = db.Column(db.String)
    type = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class GlobalChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class ClassChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)
