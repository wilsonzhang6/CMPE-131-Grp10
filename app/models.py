#provided by teach
#this is the database and database classes
from datetime import datetime
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) #integer that is incremented when a new addition is added
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    routines = db.relationship('Routine', backref='author', lazy=True)

#Registration - Set Password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} {}>'.format(self.username, self.email)    

#For password reset
    def get_reset_token(self, expire_seconds=900):
        s = Serializer(app.config['SECRET_KEY'], expire_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


#This is modified to be a routine/post
class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(2000), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

     #this is the author of the routine
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return '<Routine: {} {} {}>'.format(self.title, self.description, self.timestamp)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



'''
    def __repr__(self):
        return f"Routine('{self.title}', '{self.description}', '{self.timestamp}')"
'''