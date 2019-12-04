#provided by teach
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #essentially the directory path 

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    #directory for database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')


    #keep track of changes
    SQLALCHEMY_TRACK_MODIFICATIONS = False