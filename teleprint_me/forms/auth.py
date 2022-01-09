from flask_wtf import FlaskForm

from peewee import DoesNotExist

from teleprint_me.core import sqlite
from teleprint_me.core import scrypt

from wtforms.fields import PasswordField
from wtforms.fields import SubmitField
from wtforms.fields import EmailField
from wtforms.validators import Email
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError


class SignUpEmail(object):
    def __init__(self, message=None):
        if not message:
            message = 'User already exists'
        self.message = message

    def __call__(self, form, field):
        try:
            if sqlite.User.get(sqlite.User.name == field.data):
                raise ValidationError(self.message)
        except (DoesNotExist,):
            pass


class SignInEmail(object):
    def __init__(self, message=None):
        if not message:
            message = 'Email is invalid'
        self.message = message

    def __call__(self, form, field):
        try:
            if sqlite.User.get(sqlite.User.name == form.email.data):
                pass
        except (DoesNotExist,):
            raise ValidationError(self.message)


class SignInPassword(object):
    def __init__(self, message=None):
        if not message:
            message = 'Password is invalid'
        self.message = message

    def __call__(self, form, field):
        try:
            user = sqlite.User.get(sqlite.User.name == form.email.data)
            if not scrypt.verify(user.password, field.data):
                raise ValidationError(self.message)
        except (DoesNotExist,):
            raise ValidationError(self.message)


class SignUpForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Length(min=5, message='Email must be at least 5 characters long'),
        Email(message='Email must be valid'),
        SignUpEmail()
    ])
    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('repeat', 'Passwords must match')
    ])
    repeat = PasswordField('Repeat Password', [
        DataRequired(message='Password repeat is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    submit = SubmitField('Sign up')


class SignInForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Email(message='Email must be valid'),
        SignInEmail()
    ])
    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        SignInPassword()
    ])
    submit = SubmitField('Sign in')
