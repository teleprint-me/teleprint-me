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
from ledger.core import scrypt
from ledger.core import mongo

from ledger.forms.auth import SignUpForm
from ledger.forms.auth import SignInForm

from ledger.exchange.cbpro.client import CoinbaseProFactory
from ledger.exchange.kraken.client import KrakenFactory

from flask import render_template
from flask import flash
from flask import g
from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask import Blueprint

import bson
import functools
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')


class User(object):
    def __init__(self, objectid):
        document = mongo.db.users.find_one({'_id': objectid})
        self.__oid = objectid
        self.email = document['email']
        self.password = document['password']
        self.database = document['database']

        self.tokens = []
        self.clients = []

    @property
    def objectid(self):
        return self.__objectid


def required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            path = url_for('auth.sign_in')
            return redirect(path)
        return view(**kwargs)
    return wrapped_view


def redirect_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            path = url_for('index')
            return redirect(path)
        return view(**kwargs)
    return wrapped_view


def get_user():
    _id = session.get('sid')
    objectid = bson.objectid.ObjectId(_id)
    return mongo.db.users.find_one({'_id': objectid})


def get_database(user):
    if user:
        key = str(user['database'])
        return mongo.cx[key]
    return None


def get_client(cursor):
    platform = cursor.get('platform')
    key = cursor.get('key')
    secret = cursor.get('secret')
    passphrase = cursor.get('passphrase')
    if platform == 'coinbase-pro':
        return CoinbaseProFactory().get_client(key, secret, passphrase)
    if platform == 'kraken':
        return KrakenFactory().get_client(key, secret)
    return None


def get_accounts(db):
    accounts = list()
    if db:
        for account in db.accounts.find():
            client = get_client(account)
            if client:
                accounts.append(client)
    return accounts


@bp.before_app_request
def load_user_session():
    g.user = get_user()
    g.db = get_database(g.user)
    g.accounts = get_accounts(g.db)


@bp.route('/sign-up', methods=('GET', 'POST'))
@redirect_user
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            session.clear()
            result = mongo.db.users.insert_one({
                'database': uuid.uuid4(),
                'email': form.email.data,
                'password': scrypt.hash(form.password.data),
                'verified': False,
                '2fa': False
            })
            session['sid'] = str(result.inserted_id)
            path = url_for('index')
            return redirect(path)
        for key, value in form.errors.items():
            if value:
                messages.append((key, value[0]))
        if messages:
            flash(tuple(messages))
    return render_template('auth/sign-up.html', form=form)


@bp.route('/sign-in', methods=('GET', 'POST'))
@redirect_user
def sign_in():
    form = SignInForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            document = mongo.db.users.find_one({'email': form.email.data})
            session.clear()
            session['sid'] = str(document['_id'])
            return redirect(url_for('index'))
        for key, value in form.errors.items():
            if value:
                messages.append((key, value[0]))
        if messages:
            flash(tuple(messages), 'error')
    return render_template('auth/sign-in.html', form=form)


@bp.route('/sign-out')
def logout():
    session.clear()
    path = url_for('auth.sign_in')
    return redirect(path)
