from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from peewee import DoesNotExist

from teleprint_me.blueprints import auth
from teleprint_me.core import Interface
from teleprint_me.forms.interfaces import InterfaceCreateForm

blueprint = Blueprint('interfaces', __name__, url_prefix='/interfaces')


def get_interface(name: str) -> Interface:
    try:
        return Interface.get(Interface.name == name)
    except (DoesNotExist,):
        return None


@blueprint.route('/menu', methods=('GET',))
@auth.required
def menu():
    return render_template('interfaces/menu.html')


@blueprint.route("/create", methods=('GET', 'POST'))
@auth.required
def create():
    form = InterfaceCreateForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            interface = Interface.create(
                name=form.name.data,
                key=form.key.data,
                secret=form.secret.data,
                passphrase=form.passphrase.data,
                rest=form.rest.data,
                feed=form.feed.data,
                active=True if 'on' == form.active.data else False,
                user=g.user
            )
            if 1 == interface.save():
                messages.append(
                    ('Create', f'Created {interface.name}'))
            else:
                messages.append(
                    ('Error', f'Failed to create {interface.name}'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('interfaces.create'))
    return render_template('interfaces/create.html', form=form)


@blueprint.route('/read', methods=(('GET',)))
@auth.required
def read():
    name = request.args.get('name')
    interface = get_interface(name)
    if name and interface:
        for i in g.interfaces:
            if i == interface:
                i.active = True
            else:
                i.active = False
        Interface.bulk_update(g.interfaces, fields=[Interface.active])
        messages = [('Update', f'Using {interface.name}')]
        flash(tuple(messages), 'info')
        return redirect(url_for('interfaces.read'))
    return render_template('interfaces/read.html', interfaces=g.interfaces)


@blueprint.route('/delete', methods=('GET', 'POST'))
@auth.required
def delete():
    name = request.args.get('name')
    interface = get_interface(name)
    if name and interface:
        if not interface.active:
            messages = [('Delete', f'Deleted {interface.name}')]
            interface.delete_instance()
        else:
            messages = [('Error', f'Using {interface.name}')]
        flash(tuple(messages), 'info')
        return redirect(url_for('interfaces.delete'))
    return render_template('interfaces/delete.html', interfaces=g.interfaces)
