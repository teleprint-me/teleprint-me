from flask_wtf import FlaskForm
from wtforms.fields import PasswordField
from wtforms.fields import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError

from ledger.core import scrypt
from ledger.core import mongo


#
# Registration
#
class SignUpEmail(object):
    def __init__(self, message=None):
        if not message:
            message = 'Email already exists'
        self.message = message

    def __call__(self, form, field):
        document = mongo.db.users.find_one({'email': field.data})
        if document:
            raise ValidationError(self.message)


class SignUpForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Length(min=6, message='Email must be at least 6 characters long'),
        Email(message='Email must be valid'),
        SignUpEmail()
    ])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('repeat', 'Passwords must match')
    ])

    repeat = PasswordField('Repeat Password')

    submit = SubmitField('Sign up')


#
# Login
#
class SignInEmail(object):
    def __init__(self, message=None):
        if not message:
            message = 'Email does not exist'
        self.message = message

    def __call__(self, form, field):
        document = mongo.db.users.find_one({'email': field.data})
        if not document:
            raise ValidationError(self.message)


class SignInPassword(object):
    def __init__(self, message=None):
        if not message:
            message = 'Password is invalid'
        self.message = message

    def __call__(self, form, field):
        document = mongo.db.users.find_one({'email': form.email.data})
        if not document or not scrypt.verify(field.data, document['password']):
            raise ValidationError(self.message)


class SignInForm(FlaskForm):
    email = EmailField('Email', [
        DataRequired(message='Email is required'),
        Length(min=6, message='Email must be at least 6 characters long'),
        Email(message='Email must be valid'),
        SignInEmail()
    ])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        SignInPassword()
    ])

    submit = SubmitField('Sign in')
