from flask_wtf import FlaskForm

from peewee import DoesNotExist

from wtforms.fields import SelectField
from wtforms.fields import StringField
from wtforms.fields import SubmitField
from wtforms.fields import FloatField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from wtforms.widgets.html5 import NumberInput

from teleprint_me.core import Strategy


class StrategyExists(object):
    def __init__(self, message=None):
        if not message:
            message = 'Strategy already exists'
        self.message = message

    def __call__(self, form, field):
        try:
            if Strategy.get(Strategy.alias == field.data):
                raise ValidationError(self.message)
        except (DoesNotExist,):
            pass


class StrategyForm(FlaskForm):
    name = StringField('Name', [
        DataRequired('Strategy Name is required'), StrategyExists()])
    product = StringField('Product', [
        DataRequired('Product ID is required')])
    principal = FloatField('Principal', [
        DataRequired('Principal Amount is required')
    ], widget=NumberInput(step=1, min=0))
    type_ = SelectField('Type', [
        DataRequired('Strategy Type is required'),
    ], choices=[
        ('', 'Type'),
        ('cost_average', 'Cost Average'),
        ('dynamic_cost_average', 'Dynamic Cost Average'),
        ('value_average', 'Value Average'),
        ('dynamic_value_average', 'Dynamic Value Average')
    ])
    frequency = SelectField('Frequency', [
        DataRequired('Trade Frequency is required'),
    ], choices=[
        ('', 'Frequency'),
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ])
    yield_ = SelectField('Yield', choices=[('', 'Yield')] + [
        (y / 100, f'{y}%') for y in list(range(5, 13))
    ])
    submit = SubmitField('Create Strategy')
