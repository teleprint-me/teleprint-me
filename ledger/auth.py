from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from bson.objectid import ObjectId

from ledger.core.security import shash
from ledger.core.security import sverify
from ledger.core.extensions import mongo

import functools
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')


def required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_user_session() -> None:
    _id = session.get('sid')
    g.user = mongo.db.users.find_one({'_id': ObjectId(_id)})
    if g.user:
        key = str(g.user['database'])
        g.db = mongo.cx[key]


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        message = None
        email = request.form.get('email')
        password = request.form.get('password')
        repeat = request.form.get('repeat')
        document = mongo.db.users.find_one({'email': email})

        if not email:
            message = 'Username is required'
        elif not password:
            message = 'Password is required'
        elif not repeat:
            message = 'Password Repeat is required'
        elif password != repeat:
            message = 'Passwords do not match'
        elif document:
            message = f'{email} is already registered'

        if message is None:
            session.clear()
            result = mongo.db.users.insert_one({
                'database': uuid.uuid4(),
                'email': email,
                'password': shash(password),
                'verified': False,
                '2fa': False
            })
            session['sid'] = str(result.inserted_id)
            return redirect(url_for('index'))

        flash(('Error', message))

    return render_template('auth/register.html')


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        print('[LOGIN] receieved post request')
        message = None
        email = request.form.get('email')
        password = request.form.get('password')
        document = mongo.db.users.find_one({'email': email})

        if not email:
            message = 'A email is required'
        elif not password:
            message = 'A password is required'
        elif not document:
            message = f'Email {email} does not exist'
        elif not sverify(password, document['password']):
            message = 'Invalid password was given'

        if message is None:
            session.clear()
            session['sid'] = str(document['_id'])
            return redirect(url_for("index"))

        flash(('Error', message))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
