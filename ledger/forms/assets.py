# Ledger - A web application to track cryptocurrency investments
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from flask_wtf import FlaskForm

from wtforms.widgets.html5 import NumberInput

from wtforms.fields import SelectField
from wtforms.fields import StringField
from wtforms.fields import SubmitField
from wtforms.fields.html5 import IntegerField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from flask import g


class AssetExists(object):
    def __init__(self, message=None):
        if not message:
            message = 'Asset already exists'
        self.message = message

    def __call__(self, form, field):
        for product in g.db.assets.find():
            has_account = form.platform.data == product['platform']
            has_asset = field.data == product['asset']
            if has_account and has_asset:
                raise ValidationError(self.message)


class AssetsCreateForm(FlaskForm):
    platform = SelectField('Account', [
        DataRequired('Account is required')
    ], choices=[
        ('coinbase', 'Coinbase'),
        ('coinbase-pro', 'Coinbase Pro'),
        ('kraken', 'Kraken')
    ])

    asset = StringField('Asset', [
        DataRequired('Asset is required'),
        AssetExists()
    ])

    strategy = SelectField('Strategy', [
        DataRequired('Strategy is required'),
    ], choices=[
        ('cost-average', 'Cost Average'),
        ('dynamic-cost-average', 'Dynamic Cost Average'),
        ('value-average', 'Value Average'),
        ('dynamic-value-average', 'Dynamic Value Average')
    ])

    principle = IntegerField('Principle Amount', [
        DataRequired('Principle Amount is required')
    ], widget=NumberInput(step=5, min=5))

    period = SelectField('Period', [
        DataRequired('Period is required'),
    ], choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ])

    apy = SelectField('Annual Percentage Yield', choices=[
        ('0.05', '5%'),
        ('0.075', '7.5%'),
        ('0.10', '10%'),
        ('0.125', '12.5%'),
        ('0.15', '15%')
    ])

    submit = SubmitField('Add Asset')
