#provided by teach
#database functions, initializes flask objects
import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):

    app = Flask(__name__)
    mail = Mail(app)


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

    #For password reset
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True

    #SET Environment variable or hard code in a gmail account
    app.config['MAIL_USERNAME'] = 'taskroutecmpe131@gmail.com'
    app.config['MAIL_PASSWORD'] = '15spLW#GY*m6'

    # here are all the pieces of my program
    with app.app_context():
        from . import routes
        db.create_all()

    return app