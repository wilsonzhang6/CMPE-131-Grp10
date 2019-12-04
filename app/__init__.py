#provided by teach 
#database functions, initializes flask objects
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

#flask object
app = Flask(__name__)
app.config.from_object(Config)

#database
db = SQLAlchemy(app) #instantiation

#login
login = LoginManager(app)
# right side is the function that's called to login users
login.login_view = 'login'

#For password reset
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

#SET Environment variable or hard code in a gmail account
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

#import models (tables) for database
from app import routes, models