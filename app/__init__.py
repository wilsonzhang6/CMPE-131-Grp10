#provided by teach 
#database functions, initializes flask objects
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#flask object
app = Flask(__name__)
app.config.from_object(Config)

#database
db = SQLAlchemy(app) #instantiation

#login
login = LoginManager(app)
    # right side is the function that's called to login users
login.login_view = 'login'

#import models (tables) for database
from app import routes, models