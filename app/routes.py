#provided by teach
#routes URL
from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import CreateRoutineForm
from app.models import User
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')

#Home page
@app.route('/home') 
def home():
     return render_template('home.html', title='Home') #problem

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # look at first result first()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return to page before user got asked to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

#Logout function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#User's home page
@app.route('/index')
@login_required
def index():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('index.html', title='User Home', image_file=image_file)#, posts=posts)

#page to upload a profile picture (another feature)
@app.route('/index/profilepic')
@login_required
def profilepic():
    #add functionality here
    return render_template('profilepic.html', title='Upload Profile Picture')

#Routine creation
#This is entirely UNTESTED
@app.route('/createroutine', methods=['GET', 'POST'])
@login_required
def createRoutine():
    form = CreateRoutineForm()
    title = Title(title=form.title.data)
    desc = Desc(description=form.description.data)
    return render_template('createroutine.html', title='Create Routine', form = form)