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

from wtforms.fields import SelectField
from wtforms.fields import StringField
from wtforms.fields import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from flask import g


class AccountExists(object):
    def __init__(self, message=None):
        if not message:
            message = 'Account already exists'
        self.message = message

    def __call__(self, form, field):
        for account in g.db.accounts.find():
            if account['platform'] == field.data:
                raise ValidationError(self.message)


class AccountsCreateForm(FlaskForm):
    platform = SelectField('Platform', [
        DataRequired('Platform is required'),
        AccountExists()
    ], choices=[
        ('coinbase', 'Coinbase'),
        ('coinbase-pro', 'Coinbase Pro'),
        ('kraken', 'Kraken')
    ])

    key = StringField('Key', [DataRequired('Key is required')])

    secret = StringField('Secret', [DataRequired('Secret is required')])

    passphrase = StringField('Passphrase')

    submit = SubmitField('Add Account')
