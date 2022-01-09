from flask_wtf import FlaskForm

from wtforms.fields import BooleanField
from wtforms.fields import StringField
from wtforms.fields import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from flask import g


class ValidateName(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API Name already exists'
        self.message = message

    def __call__(self, form, field):
        for interface in g.user.interfaces:
            if interface.name == field.data:
                raise ValidationError(self.message)


class ValidateKey(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API Key already exists'
        self.message = message

    def __call__(self, form, field):
        for interface in g.user.interfaces:
            if interface.key == field.data:
                raise ValidationError(self.message)


class ValidateRest(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API REST URL is invalid'
        self.message = message

    def __call__(self, form, field):
        whitelist = [
            'https://api.pro.coinbase.com',
            'https://api-public.sandbox.pro.coinbase.com',
            'https://api.exchange.coinbase.com',
            'https://api-public.sandbox.exchange.coinbase.com'
        ]
        if field.data not in whitelist:
            raise ValidationError(self.message)


class ValidateFeed(object):
    def __init__(self, message: str = None):
        if not message:
            message = 'API FEED URL is invalid'
        self.message = message

    def __call__(self, form, field):
        whitelist = [
            'wss://ws-feed.pro.coinbase.com',
            'wss://ws-feed.exchange.coinbase.com'
        ]
        if field.data not in whitelist:
            raise ValidationError(self.message)


# TODO: deprecate the active field from the interface form
class InterfaceForm(FlaskForm):
    name = StringField('Name', [DataRequired('Name is required'), ValidateName()])
    key = StringField('Key', [DataRequired('Key is required'), ValidateKey()])
    secret = StringField('Secret', [DataRequired('Secret is required')])
    passphrase = StringField('Passphrase', [DataRequired('Passphrase is required')])
    rest = StringField(
        'Interface', [ValidateRest()], default='https://api.pro.coinbase.com')
    feed = StringField(
        'Feed', [ValidateFeed()], default='wss://ws-feed.pro.coinbase.com')
    active = BooleanField('Inactive Profile', default=True)
    submit = SubmitField('Add Account')
