#provided by teach
#database functions, initializes flask objects
import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        #app.config.from_pyfile('config.py', silent=True)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # here are all the pieces of my program
    with app.app_context():
        from . import routes
        db.create_all()

    return app



'''
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
'''
