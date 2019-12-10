#provided by teach
#different forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User, Routine
import calendar

#Form for logging into system
class LoginForm(FlaskForm):
    """ This is the Form used for user Login
        
        :param FlaskForm: WTForm API
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Form for new account registration
class RegistrationForm(FlaskForm):
    """ This is the Form used for user Login
        
        :param FlaskForm: WTForm API
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """ Method used to validate inputted username from form
        
        :param username: user's username
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """ Method used to validate inputted username from form
        
        :param username: user's username
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

#Form for creating Routine
class CreateRoutineForm(FlaskForm):
    """ This is the form used to create a routine. User must be logged in to create said routine. 
        
        :param FlaskForm: WTForm API
    """

    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_maxtitle(self, title):
        """ Method used to limit the number of characters up to 100
            
            :param title (String): The desired title of the routine
        """
        if len(title) > 100:
            raise ValidationError('You have ', len(title), ' characters, the maximum is 100 characters')
    def validate_maxdesc(self, description):
        """ Method used to limit the number of characters up to 2000
            
            :param description (String): The desired description of the routine
        """
        if len(description) > 2000:
            raise ValidationError('You have ', len(description), ' characters, the maximum is 2000 characters')

#Form for new account registration
class UpdateAccountForm(FlaskForm):
    """ This form is used to update user's account details
            
        :param FlaskForm: WTForms API
    """
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        """ Method used to check & verify that it is the correct account username that is being updated
            
            :param username (StringField): username that is to be updated
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """ Method used to check & verify that it is the correct account email that is being updated
            
        :param email (StringField): email that is to be updated
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

#Form to request reset password
class RequestResetForm(FlaskForm):
    """ This form is used to request a reset password link 
            
        :param FlaskForm: WTForms API

        
    """

    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        """ Method used to check & verify that it is the correct account email that is being updated
            
        :param email (StringField): email that is to be updated

        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No such account with said email exists')

#Form to reset password
class ResetPasswordForm(FlaskForm):
    """ This form is used to reset user's account password
            
        :param FlaskForm: WTForms API
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

#Search-NotWorking
class searchForm(FlaskForm):
    """ This form is used for global search functionality
            
        :param FlaskForm: WTForms API
    """
    routineName = StringField('Search routine', validators=[DataRequired()])
    submit = SubmitField('Search')
