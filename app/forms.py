#provided by teach
#different forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Routine
import calendar

#Form for logging into system
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Form for new account registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField( 'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

#Form for creating Routine
class CreateRoutineForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #description = StringField('Description', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Routine')

    def validate_maxtitle(self, title):
        if len(title) > 100:
            raise ValidationError('You have ', len(title), ' characters, the maximum is 100 characters')
    def validate_maxdesc(self, description):
        if len(description) > 2000:
            raise ValidationError('You have ', len(description), ' characters, the maximum is 2000 characters')
'''
class ViewRoutineForm(FlaskForm):
    title=StringField('something')
    description = StringField('description')
    submit=SubmitField('View Routine')
'''
#Form for new account registration
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')
'''
#Search-NotWorking
class searchForm(FlaskForm):
    routineName = StringField('Search routine', validators=[DataRequired()])
'''
