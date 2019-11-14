from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import CreateRoutineForm
from app.forms import CreateTaskForm
from app.models import User, Routine
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/MyAccount', methods=['GET', 'POST'])
@login_required
def myAccount():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('myAccount.html', title='My Account')


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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
        flash('Congratulations, you have created an account!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateRoutineForm()
    taskform = CreateTaskForm()
    tasks = []
    if taskform.validate_on_submit():
        task = Task(taskname = form.task.data)
        tasks.append(task)
    if form.validate_on_submit():
        routine = Routine(routinetitle = form.title.data)
        db.session.add(routine)
        db.session.commit()
        flash('Congratulations, you have created a routine!')
        return redirect(url_for('index'))
    return render_template('createroutine.html', title='Create', form=form, taskform=taskform)

@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('viewroutine.html', title='View')
