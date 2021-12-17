from teleprint_me.core import scrypt
from teleprint_me.core import User
from teleprint_me.core import Interface

from teleprint_me.forms.auth import SignUpForm
from teleprint_me.forms.auth import SignInForm

from coinbase_pro.client import Client
from coinbase_pro.client import get_client

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask_wtf import FlaskForm

from peewee import ModelSelect
from peewee import OperationalError
from peewee import DoesNotExist

import functools

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


def error(form: FlaskForm, messages: list) -> list:
    for key, value in form.errors.items():
        try:
            messages.append((key, value[0]))
        except (IndexError,) as e:
            messages.append(('Error', e))
    return messages


def required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.sign_in'))
        return view(**kwargs)
    return wrapped_view


def redirect_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view


def load_user_interface(interfaces: ModelSelect) -> Interface:
    try:
        return [i for i in interfaces if i.active][0]
    except (IndexError,):
        return None


def load_user_client(interface: Interface) -> Client:
    try:
        return get_client({
            'key': interface.key,
            'secret': interface.secret,
            'passphrase': interface.passphrase,
            'authority': interface.rest
        })
    except (AttributeError,):
        return None


@blueprint.before_app_request
def load_user_session():
    try:
        g.user = User.get(User.sid == session.get('sid'))
        g.interfaces = g.user.interfaces
        g.strategies = g.user.strategies
        g.interface = load_user_interface(g.interfaces)
        g.client = load_user_client(g.interface)
    except (DoesNotExist,):
        g.user = None


@blueprint.route('/sign-up', methods=('GET', 'POST'))
@redirect_user
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            try:
                session.clear()
                hashed = scrypt.hash(form.password.data)
                user = User.create(name=form.email.data, password=hashed)
                user.save()
                session['sid'] = user.sid
                return redirect(url_for('index'))
            except (OperationalError,) as e:
                messages.append(('Database', e))
        messages = error(form, messages)
        if messages:
            flash(tuple(messages), 'error')
    return render_template('auth/sign-up.html', form=form)


@blueprint.route('/sign-in', methods=('GET', 'POST'))
@redirect_user
def sign_in():
    form = SignInForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            try:
                session.clear()
                user = User.get(User.name == form.email.data)
                session['sid'] = user.sid
                return redirect(url_for('index'))
            except (OperationalError,) as e:
                messages.append(('Database', e))
        messages = error(form, messages)
        if messages:
            flash(tuple(messages), 'error')
    return render_template('auth/sign-in.html', form=form)


@blueprint.route('/sign-out')
def sign_out():
    session.clear()
    return redirect(url_for('auth.sign_in'))
