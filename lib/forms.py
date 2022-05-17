
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError, EqualTo
from .models import User



class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class registerForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)]) 
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email")])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must be register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
