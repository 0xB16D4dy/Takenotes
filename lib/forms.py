from flask_wtf import FlaskForm
from flask_login import current_user
from sqlalchemy import false
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError, EqualTo, regexp
from .models import User
import re 


def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("Remeber Me")

    def validate_username(self, username):
        excluded_chars = "*?!'^+%&/()=}][{$-#\";"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")
                    
        user = User.query.filter_by(user_name = username.data).first()
        if not user:
            raise ValidationError("The user doesn't exist, please check again")
    
        
           

class registerForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="fill required"), Email(message="Invalid email"), Length(max=50)]) 
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(message="fill required"), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

    def validate_username(self, username):
        user = User.query.filter_by(user_name = username.data).first()
        if user:
            raise ValidationError("This username already exists, please choose another username")
        else:
            excluded_chars = "*?!'^+%&/()=}][{$-#"
            for char in self.username.data:
                if char in excluded_chars:
                    raise ValidationError(
                        f"Character {char} is not allowed in username.")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exists, please choose another email")
        elif (is_email_address_valid(email.data) == false):
            raise ValidationError("Invalid email, please check again")
            

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email")])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must be register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[ FileRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.user_name:
            user = User.query.filter_by(user_name=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
