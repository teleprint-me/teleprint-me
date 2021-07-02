from flask_wtf import FlaskForm
from wtforms.fields import PasswordField
from wtforms.fields import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length


class SignInForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Length(min=6, message='Email must be at least 6 characters long'),
        Email(message='Email must be valid')
    ])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Length(min=6, message='Email must be at least 6 characters long'),
        Email(message='Email must be valid')
    ])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('repeat', 'Passwords must match')
    ])

    repeat = PasswordField('Repeat Password')

    submit = SubmitField('Sign up')
