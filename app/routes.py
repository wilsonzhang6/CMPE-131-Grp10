from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import CreateRoutineForm
from app.models import User, Todo
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy

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

'''    
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateRoutineForm()
    return render_template('createroutine.html', title='Create', form=form)
'''    
@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('viewroutine.html', title='View')

@app.route('/create', methods=['GET''POST'])
def create():
    incomplete=Todo.query.filter_by(complete=False).all()
    complete=Todo.query.filter_by(complete=True).all()
    return render_template('createroutine.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))   

@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('createroutine'))    

'''
@app.route('/create', methods=['GET','POST'])
def create():
    incomplete= Task.query.filter_by(mon=False).all()
    mon=Task.query.filter_by(mon=True).all()
    tue=Task.query.filter_by(tue=True).all()
    wed=Task.query.filter_by(wed=True).all()
    thu=Task.query.filter_by(thu=True).all()
    fri=Task.query.filter_by(fri=True).all()
    sat=Task.query.filter_by(sat=True).all()
    sun=Task.query.filter_by(sun=True).all()
    
    return render_template('createroutine.html', incomplete=incomplete, complete=complete)
    
    #return render_template('createroutine.html', incomplete=incomplete, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, sun=sun)
@app.route('/add', methods=['POST'])
def add():
    #task = Task(task=request.form['task-name'], mon=False, tue=False, wed=False, thu=False, fri=False, sat=False, sun=False)
    task = Task(task=request.form['task-name'], complete=False)    
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('createroutine'))
@app.route('/complete/<id>')
def mon(id):

    task = Task.query.filter_by(id=int(id)).first()
    task.complete = True
    db.session.commit()
    
    return redirect(url_for('createroutine'))    
'''
'''
@app.route('/create', methods=['GET', 'POST'])
def create():
    
    tasks = Task(task=request.form['task-name'], mon=False,tue=False, wed=False, thu=False, fri=False, sat=False, sun=False)
    db.session.add(tasks)
    db.session.commit()

    return redirect(url_for('createroutine'))
'''