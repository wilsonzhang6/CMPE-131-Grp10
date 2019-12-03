<<<<<<< HEAD
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
=======
#provided by teach
#routes URL
from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateRoutineForm, UpdateAccountForm
from app.models import User, Routine
from flask_login import current_user, login_user, logout_user, login_required
>>>>>>> a17421f... added viewroutine/create new routine/update routine/delete routine
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


<<<<<<< HEAD
=======
@app.route("/viewroutine")
def viewroutine():
    routines= Routine.query.all()
    return render_template('viewroutine.html', routines=routines)

#Login page
>>>>>>> a17421f... added viewroutine/create new routine/update routine/delete routine
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

<<<<<<< HEAD
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
=======
#To be used to save a profile picture -> to update a user's profile picture
#Currently used by index() function
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #randomize the new uploaded picture file name
    picture_fn = random_hex + f_ext #randomized picture file name + original uploaded file extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path) #save the picture

    #Reduce the size of the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#User's account page, currently includes a form that allows user to update personal info
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = UpdateAccountForm() #Form to update account
    if form.validate_on_submit(): #After submission button is inputted
        if form.picture.data: #if the form has picture data input
            current_user.image_file = save_picture(form.picture.data)#pass the uploaded picture in order to save
            #current_user.image_file = picture_file #replace the current user's image with the one uploaded
        current_user.username = form.username.data #replace the current user's username iwth the one inputted by form
        current_user.email = form.email.data #replace the current user's email with the email that was inputted by form
        db.session.commit() #commit all changes into the database
        flash('your account information has been updated!', 'success') #message flash
        return redirect(url_for('index')) #redirect user back to the index page
    elif request.method == 'GET': #When the page requests a GET (such as when the page loads in the browser)
        form.username.data = current_user.username #pre-fill the form field with the user's current username
        form.email.data = current_user.email #pre-fill the form field with the user's current email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('index.html', title='User Home', image_file=image_file, form=form)

#Routine creation
#This is TESTED
#needs submit button
@app.route('/routine/new', methods=['GET', 'POST'])
@login_required
def createRoutine():
    form = CreateRoutineForm()
    if form.validate_on_submit(): #added this part
        #tasks = Routine(title=form.title.data, description=form.description.data, timestamp=date.today())
        routine = Routine(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(routine)
        db.session.commit()
        flash('Your routine has been created!', 'success')
        return redirect(url_for('viewroutine'))
   # routine = Routine.query.filter_by(title=title.form.data).first()
    #title = Routine(title=form.title.data)
    #desc = Routine(description=form.description.data)
    return render_template('createtask.html', title='Create Routine', form = form, legend='New Routine')

@app.route("/routine/<int:routine_id>")
def routine(routine_id):
    routine= Routine.query.get_or_404(routine_id)
    return render_template('routine.html', title=routine.title,routine=routine)

@app.route("/routine/<int:routine_id>/update", methods=['GET', 'POST'])
@login_required
def update_routine(routine_id):
    routine = Routine.query.get_or_404(routine_id)
    if routine.author != current_user:
        abort(403)
    form = CreateRoutineForm()
    if form.validate_on_submit():
        routine.title = form.title.data
        routine.description = form.description.data
        db.session.commit()
        flash('Your routine has been updated!', 'success')
        return redirect(url_for('routine', routine_id=routine.id))
    elif request.method == 'GET':
        form.title.data = routine.title
        form.description.data = routine.description
    return render_template('createtask.html', title='Update Routine',
                           form=form, legend='Update Routine')


@app.route("/routine/<int:routine_id>/delete", methods=['POST'])
@login_required
def delete_routine(routine_id):
    routine = Routine.query.get_or_404(routine_id)
    if routine.author != current_user:
        abort(403)
    db.session.delete(routine)
    db.session.commit()
    flash('Your routine has been deleted!', 'success')
    return redirect(url_for('viewroutine'))
>>>>>>> a17421f... added viewroutine/create new routine/update routine/delete routine
