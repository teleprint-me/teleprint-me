from flask_wtf import FlaskForm

from wtforms.fields import BooleanField
from wtforms.fields import StringField
from wtforms.fields import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from flask import g


class NameExists(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API Name already exists'
        self.message = message

    def __call__(self, form, field):
        for interface in g.interfaces:
            if interface.name == field.data:
                raise ValidationError(self.message)


class KeyExists(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API Key already exists'
        self.message = message

    def __call__(self, form, field):
        for interface in g.interfaces:
            if interface.key == field.data:
                raise ValidationError(self.message)


class InterfaceCreateForm(FlaskForm):
    name = StringField('Name', [DataRequired('Name is required'), NameExists()])
    key = StringField('Key', [DataRequired('Key is required'), KeyExists()])
    secret = StringField('Secret', [DataRequired('Secret is required')])
    passphrase = StringField('Passphrase', [DataRequired('Passphrase is required')])
    rest = StringField('Interface')
    feed = StringField('Feed')
    active = BooleanField('Inactive Profile')
    submit = SubmitField('Add Account')
