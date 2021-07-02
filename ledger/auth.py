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
from ledger.forms import SignUpForm
from ledger.forms import SignInForm

from ledger.core.security import shash
from ledger.core.extensions import mongo

from ledger.client.coinbasepro import CoinbaseProFactory
from ledger.client.kraken import KrakenFactory

import bson
import flask
import functools
import uuid

bp = flask.Blueprint('auth', __name__, url_prefix='/auth')


def required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            path = flask.url_for('auth.sign_in')
            return flask.redirect(path)
        return view(**kwargs)
    return wrapped_view


def redirect_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is not None:
            path = flask.url_for('index')
            return flask.redirect(path)
        return view(**kwargs)
    return wrapped_view


def get_user():
    _id = flask.session.get('sid')
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
    flask.g.user = get_user()
    flask.g.db = get_database(flask.g.user)
    flask.g.accounts = get_accounts(flask.g.db)


@bp.route('/sign-up', methods=('GET', 'POST'))
@redirect_user
def sign_up():
    form = SignUpForm(flask.request.form)
    if flask.request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            flask.session.clear()
            result = mongo.db.users.insert_one({
                'database': uuid.uuid4(),
                'email': form.email.data,
                'password': shash(form.password.data),
                'verified': False,
                '2fa': False
            })
            flask.session['sid'] = str(result.inserted_id)
            path = flask.url_for('index')
            return flask.redirect(path)
        for key, value in form.errors.items():
            if value:
                messages.append((key, value[0]))
        if messages:
            flask.flash(tuple(messages))
    return flask.render_template('auth/sign-up.html', form=form)


@bp.route('/sign-in', methods=('GET', 'POST'))
@redirect_user
def sign_in():
    form = SignInForm(flask.request.form)
    if flask.request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            document = mongo.db.users.find_one({'email': form.email.data})
            flask.session.clear()
            flask.session['sid'] = str(document['_id'])
            return flask.redirect(flask.url_for('index'))
        for key, value in form.errors.items():
            if value:
                messages.append((key, value[0]))
        if messages:
            flask.flash(tuple(messages), 'error')
    return flask.render_template('auth/sign-in.html', form=form)


@bp.route('/sign-out')
def logout():
    flask.session.clear()
    path = flask.url_for('auth.sign_in')
    return flask.redirect(path)
