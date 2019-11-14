#provided by teach
#this is the database and database classes
from datetime import datetime
from app import db #import from upper directory level
from app import login #import from upper directory level
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) #integer that is incremented when a new addition is added

    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    routines = db.relationship('Routine', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} {}>'.format(self.username, self.email)    

#This is modified to be a routine/post
class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #this is the author of the routine
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(2000), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Routine: {} {}>'.format(self.title, self.description)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
'''
from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #tasks=db.relationship('Task', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Posts {}>'.format(self.body)

#class Task(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  taskname = db.Column(db.String(128), index=True)
   # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   # mon = db.Column(db.Boolean, unique=False, default=True)
   # tue = db.Column(db.Boolean, unique=False, default=True)
   # wed = db.Column(db.Boolean, unique=False, default=True)
   # thu = db.Column(db.Boolean, unique=False, default=True)
   # fri = db.Column(db.Boolean, unique=False, default=True)
   # sat = db.Column(db.Boolean, unique=False, default=True)
   # sun = db.Column(db.Boolean, unique=False, default=True)

    #def __repr__(self):
    #    return '<Tasks {}>'.format(self.taskname)

# class Routine(db.Model):    #made up of Task classes
 #   routinetitle = db.Column(db.String())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''