from flask import Flask, url_for, redirect, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


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
    id = db.Column(db.Integer, db.ForeignKey('auth.id'), primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    class_ = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class GlobalChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    text = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class ClassChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)


events = [{'date': '24 февраля', 'subject': 'Физика', 'type': 'самостоятельная', 'prepare': 'параграфы 15-17wqdqwqewdqwdqwdqwdqwdqwdqwdqwdqwdqwddqwdqwd'},
          {'date': '24 февраля', 'subject': 'Алгебра',
              'type': 'контрольная', 'prepare': 'параграфы 15-17wqdqwdwqd'},
          {'date': '24 февраля', 'subject': 'Алгебра', 'type': 'контрольная',
              'prepare': 'параграфы 15-1dqwdqwdqwdqwd7'},
          {'date': '24 февраля', 'subject': 'Алгебра', 'type': 'контрольная', 'prepare': 'параграфы 15-1qwdqwdqwdqwd 7'}]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', events=events, username='Тестовый пользователь')


if __name__ == "__main__":
    app.run(port=8080, host='localhost', debug=True)
