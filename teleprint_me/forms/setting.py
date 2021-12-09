from teleprint_me.core import scrypt
from teleprint_me.core import User
from teleprint_me.forms.auth import SignUpEmail
from teleprint_me.forms.auth import SignInEmail

from flask import session

from flask_wtf import FlaskForm

from peewee import DoesNotExist

from wtforms.fields import BooleanField
from wtforms.fields import PasswordField
from wtforms.fields import SelectField
from wtforms.fields import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError


class ValidatePassword(object):
    def __init__(self, message=None):
        if not message:
            message = 'Password is invalid'
        self.message = message

    def __call__(self, form, field):
        try:
            user = User.get(User.sid == session.get('sid'))
            if not scrypt.verify(user.password, field.data):
                raise ValidationError(self.message)
        except (DoesNotExist,):
            raise ValidationError(self.message)


class EmailForm(FlaskForm):
    email = EmailField('Current Email', [
        DataRequired(message='Email is required'),
        Length(min=5, message='Email must be at least 5 characters long'),
        Email(message='Email must be valid'),
        SignInEmail()
    ])
    new = EmailField('New Email', [
        DataRequired(message='New email is required'),
        Length(min=5, message='New email must be at least 5 characters long'),
        EqualTo('repeat', 'Emails must match'),
        SignUpEmail()
    ])
    repeat = EmailField('Repeat New Email', [
        DataRequired(message='Repeat of new email is required'),
        Length(min=5, message='Repeat of new email must be at least 5 characters long'),
    ])
    submit = SubmitField('Save')


class PasswordForm(FlaskForm):
    password = PasswordField('Current Password', [
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        ValidatePassword()
    ])
    new = PasswordField('New Password', [
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('repeat', 'Passwords must match')
    ])
    repeat = PasswordField('Repeat New Password', [
        DataRequired(message='Repeat of new password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    submit = SubmitField('Save')


class KeyForm(FlaskForm):
    key = PasswordField('Key', [
        DataRequired(message='Key is required'),
        Length(min=8, message='Key must be at least 8 characters long'),
        EqualTo('repeat', 'Keys must match')
    ])
    repeat = PasswordField('Repeat', [
        DataRequired(message='Repeat of key is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    submit = SubmitField('Save')


class SettingForm(FlaskForm):
    currency = SelectField('Quote Currency', [
        DataRequired('Currency is required')
    ], choices=[
        ('', 'Currency'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
        ('EUR', 'EUR'),
        ('USDT', 'USDT'),
        ('USDC', 'USDC'),
        ('UST', 'UST'),
        ('DAI', 'DAI'),
        ('BTC', 'BTC'),
        ('ETH', 'ETH')
    ])
    theme = SelectField('Theme', [
        DataRequired('Theme is required')
    ], choices=[
        ('', 'Theme'),
        ('Light', 'Light'),
        ('Dark', 'Dark')
    ])
    sid = BooleanField('Reset Session Identifier')
    submit = SubmitField('Save')
