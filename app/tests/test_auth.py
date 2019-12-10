import pytest
#from app import routes, models
from app.models import User, Routine
#from collections import Iterable
#from werkzeug import url_encode
from flask import url_for
from datetime import date
from flask_login import current_user, login_user, logout_user, login_required

def test_add_user_to_db(db):
    user1 = User(username='john', email='test@test.com', password_hash='test')
    db.session.add(user1)
    db.session.commit()
    assert len(User.query.all()) == 1


def test_add_routine_to_db(db):
    user1 = User.query.filter_by(username='john').first()
    routine_1 = Routine(title='test title', description='test description & content', user_id=user1.id)
    db.session.add(routine_1)
    db.session.commit()
    assert len(Routine.query.all()) > 0


def test_update_routine(db):
    routine_1 = Routine.query.filter_by(title='test title').first()
    origuserid = routine_1.id
    routine_1.description = 'Hello There -> General Kenobi!'
    db.session.commit()
    assert routine_1.title =='test title'
    assert routine_1.description == 'Hello There -> General Kenobi!'
    assert routine_1.user_id == origuserid

def test_remove_routine_from_db(db):
    routine_1 = Routine.query.filter_by(title='test title').first()
    db.session.delete(routine_1)
    db.session.commit()
    assert len(Routine.query.all()) == 0

def test_remove_user_from_db(db):
    user1 = User.query.filter_by(username='john').first()
    db.session.delete(user1)
    db.session.commit()
    assert len(Routine.query.all()) == 0

'''
def test_valid_register(client, db):
    response = client.post(url_for('/register'), data=dict(username='testing', email='testing@testing.com', 
                                                password='testing', password2='testing'), follow_redirects=True)
    assert response.status_code == 200
    assert b'username' in response.data
    assert b'password' in response.data
'''

def test_home(client):
    response = client.get('/home')
    assert b"Login" in response.data
    #assert b"Register" in response.data

'''
def test_get_login_page(client):
    #assert client.get(url_for('login')).status_code==200
    response=client.get(url_for('/login'))
    #assert response.status_code==200
    assert b"username" in response.data
    assert b"password" in response.data
'''

def test_view_routine_page(client,db):
    response= client.get(url_for('viewroutine'), data=dict(author='john',title='test title', description='test description'), follow_redirects=True)
    assert response.status_code == 200
    #assert b'author' in response.data
    assert b'title' in response.data
    #assert b'description' in response.data

def test_view_routine_page(client):
    response= client.get('/viewroutine')
    #assert response.status_code == 200
    #assert b'author' in response.data
    assert b'title' in response.data
    #assert b'description' in response.data

def test_create_routine_page(client):
    response= client.get('/createroutine')
    #assert response.status_code == 200
    #assert b'author' in response.data
    assert b'title' in response.data
    #assert b'description' in response.data 

    

''' 
#provided by professor
import pytest
from app.models import User


def test_get_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_add_user_to_db(db):
    user1 = User(username='john', email='test@test.com', password='test')
    db.session.add(user1)
    db.session.commit()
    assert len(User.query.all()) == 1


def test_valid_register(client, db):

    response = client.post('/signup',
                                data=dict(username='testing', email='testing@testing.com', password='testing', confirm='testing'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"You are now logged in!" in response.data
    assert b'Hi !' in response.data
    assert b'Log out' in response.data


'''