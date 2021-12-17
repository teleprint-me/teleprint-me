from teleprint_me.blueprints import auth
from teleprint_me.core import scrypt
from teleprint_me.forms.setting import EmailForm
from teleprint_me.forms.setting import PasswordForm
from teleprint_me.forms.setting import KeyForm
from teleprint_me.forms.setting import SettingForm

from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from uuid import uuid4

blueprint = Blueprint('setting', __name__, url_prefix='/setting')


@blueprint.route('/menu', methods=('GET',))
@auth.required
def menu():
    return render_template('setting/menu.html')


@blueprint.route('/read', methods=('GET',))
@auth.required
def read():
    return render_template('setting/read.html')


@blueprint.route('/name', methods=('GET', 'POST'))
@auth.required
def name():
    form = EmailForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            g.user.name = form.new.data
            g.user.save()
            messages.append(('Update', 'Email updated successfully'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('setting.name'))
    return render_template('setting/name.html', form=form)


@blueprint.route('/password', methods=('GET', 'POST'))
@auth.required
def password():
    form = PasswordForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            g.user.password = scrypt.hash(form.new.data)
            g.user.save()
            messages.append(('Update', 'Password updated successfully'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('setting.password'))
    return render_template('setting/password.html', form=form)


@blueprint.route('/general', methods=('GET', 'POST'))
@auth.required
def general():
    form = SettingForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            g.user.currency = form.currency.data
            g.user.theme = form.theme.data
            if form.sid.data:
                g.user.sid = str(uuid4())
                session['sid'] = g.user.sid
            g.user.save()
            messages.append(('Update', 'General settings updated successfully'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('setting.general'))
    return render_template('setting/general.html', form=form)
