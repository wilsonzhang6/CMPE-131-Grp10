from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
<<<<<<< HEAD
    todos=db.relationship("Todo", backref="user", lazy='dynamic')
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    #tasks=db.relationship('Task', backref='author', lazy='dynamic')
=======
    #routines = db.relationship('Routine', backref='author', lazy='dynamic')
    routines = db.relationship('Routine', backref='author', lazy=True)
>>>>>>> bdefaa5... minor timestamp change

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
=======
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(2000), nullable=False)
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
>>>>>>> bdefaa5... minor timestamp change

    def __repr__(self):
        return '<Posts {}>'.format(self.body)
'''        
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), index=True)
    complete = db.Column(db.Boolean)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Todos {}>'.format(self.text)
'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mon = db.Column(db.Boolean, unique=False, default=True)
    tue = db.Column(db.Boolean, unique=False, default=True)
    wed = db.Column(db.Boolean, unique=False, default=True)
    thu = db.Column(db.Boolean, unique=False, default=True)
    fri = db.Column(db.Boolean, unique=False, default=True)
    sat = db.Column(db.Boolean, unique=False, default=True)
    sun = db.Column(db.Boolean, unique=False, default=True)

    def __repr__(self):
<<<<<<< HEAD
        return '<Tasks {}>'.format(self.taskname)
'''
'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(128), index=True)
   # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mon = db.Column(db.Boolean)
    tue = db.Column(db.Boolean)
    wed = db.Column(db.Boolean)
    thu = db.Column(db.Boolean)
    fri = db.Column(db.Boolean)
    sat = db.Column(db.Boolean)
    sun = db.Column(db.Boolean)
    '''
'''
 class Routine(db.Model):    #made up of Task classes
   routinetitle = db.Column(db.String())
'''
=======
        return '<Routine: {} {} {}>'.format(self.title, self.description, self.timestamp)
>>>>>>> bdefaa5... minor timestamp change

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
<<<<<<< HEAD
=======



'''
    def __repr__(self):
        return f"Routine('{self.title}', '{self.description}', '{self.timestamp}')"
'''
>>>>>>> bdefaa5... minor timestamp change
