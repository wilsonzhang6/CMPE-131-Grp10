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
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(2000), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

     #this is the author of the routine
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return '<Routine: {} {}>'.format(self.title, self.description)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))