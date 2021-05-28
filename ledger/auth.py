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
        error = None
        email = request.form['email']
        password = request.form['password']
        document = mongo.db.users.find_one({'email': email})

        if not email:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif document:
            error = f'{email} is already registered'

        if error is None:
            session.clear()
            result = mongo.db.users.insert({
                'email': email,
                'password': shash(password),
                'database': uuid.uuid4()
            })
            session['sid'] = result.inserted_id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        error = None
        email = request.form['email']
        password = request.form['password']
        document = mongo.db.users.find_one({'email': email})

        if document is None:
            error = f'{email} does not exist'
        elif not sverify(password, document['password']):
            error = 'invalid password was given'

        if error is None:
            session.clear()
            session['sid'] = str(document['_id'])
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
