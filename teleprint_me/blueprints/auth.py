import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf import FlaskForm
from peewee import DoesNotExist, OperationalError
from teleprint_me.core import log, scrypt, sqlite
from teleprint_me.forms.auth import SignInForm, SignUpForm
from teleprint_me.proxy import Proxy
from teleprint_me.proxy.client import ProxyClient

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def error(form: FlaskForm, messages: list) -> list:
    for key, value in form.errors.items():
        try:
            messages.append((key, value[0]))
        except (IndexError,) as e:
            messages.append(("Error", e))
    return messages


def required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for("auth.sign_in"))
        return view(**kwargs)

    return wrapped_view


def redirect_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for("index"))
        return view(**kwargs)

    return wrapped_view


@blueprint.before_app_request
def set_user_session():
    try:
        g.proxy = Proxy()
        g.user = sqlite.User.get(sqlite.User.sid == session.get("sid"))
        g.interface = g.proxy.database.interface.get_active(g.user)
        g.client = g.proxy.database.interface.get_client(g.interface)
        g.proxy.client = ProxyClient(g.client)
        log.session(g)
    except (DoesNotExist,) as e:
        g.user = None
        log.session_error(g, e)


@blueprint.route("/sign-up", methods=("GET", "POST"))
@redirect_user
def sign_up():
    form = SignUpForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            try:
                session.clear()
                hashed = scrypt.hash(form.password.data)
                user = sqlite.User.create(name=form.email.data, password=hashed)
                user.save()
                session["sid"] = user.sid
                return redirect(url_for("index"))
            except (OperationalError,) as e:
                messages.append(("Database", e))
        messages = error(form, messages)
        if messages:
            flash(tuple(messages), "error")
    return render_template("auth/sign-up.html", form=form)


@blueprint.route("/sign-in", methods=("GET", "POST"))
@redirect_user
def sign_in():
    form = SignInForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            try:
                session.clear()
                user = sqlite.User.get(sqlite.User.name == form.email.data)
                session["sid"] = user.sid
                return redirect(url_for("index"))
            except (OperationalError,) as e:
                messages.append(("Database", e))
        messages = error(form, messages)
        if messages:
            flash(tuple(messages), "error")
    return render_template("auth/sign-in.html", form=form)


@blueprint.route("/sign-out")
def sign_out():
    session.clear()
    return redirect(url_for("auth.sign_in"))
