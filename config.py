#provided by teach
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #essentially the directory path 

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    #directory for database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'user@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'password')
    MAIL_SENDER = os.environ.get('MAIL_SENDER', '<user@gmail.com>')    


    #keep track of changes
    SQLALCHEMY_TRACK_MODIFICATIONS = False