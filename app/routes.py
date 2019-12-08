#provided by teach
#routes URL
from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, CreateRoutineForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, searchForm
from app.models import User, Routine
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import secrets, os
from PIL import Image
from datetime import date
from flask_mail import Message

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
    return render_template('createtask.html', title='Update Routine', form=form, legend='Update Routine')


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

#Your Feed page
@app.route("/viewroutine", methods=['GET','POST'])
@login_required
def viewroutine():
    routines= Routine.query.all()
    return render_template('viewroutine.html', routines=routines)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='noreply@taskroute.com', 
                    recipients=[user.email])

    msg.body = f'''
    Click on the following link to reset your password:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then ignore this email
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('A password reset email has been sent')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset_Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)

    if user is None:
        flash('Invalid or Expired Token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed!')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset_Password', form=form)

#Search
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm()
    routine= Routine.query.all()
    if form.validate_on_submit():
        routine = Routine.query.filter_by(title=form.routineName.data).first()
        #routine = Routine.query.filter_by(Routine.title.like('%' + form.routineName.data + '%')).first() or Routine.query.filter(Routine.description.like('%' + form.routineName.data + '%')).first()
        return render_template('searchresults.html', routine=routine)
    return render_template('search.html', routine=routine, form=form)

#search results
@app.route('/search/searchresults', methods=['GET', 'POST'])
def searchresults(routine):
    return render_template('searchresults.html', routine=routine)
