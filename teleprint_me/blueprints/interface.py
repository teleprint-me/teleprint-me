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
from teleprint_me.forms.interface import InterfaceCreateForm

blueprint = Blueprint('interface', __name__, url_prefix='/interface')


def get_interface(name: str) -> Interface:
    try:
        return Interface.get(Interface.name == name)
    except (DoesNotExist,):
        return None


def update(interface: Interface):
    for i in g.interfaces:
        if i == interface:
            i.active = True
        else:
            i.active = False
    return Interface.bulk_update(g.interfaces, fields=[Interface.active])


@blueprint.route('/menu', methods=('GET',))
@auth.required
def menu():
    return render_template('interface/menu.html')


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
                active=form.active.data,
                user=g.user
            )
            interface.save()
            if g.interfaces:
                update(interface)
            messages.append(('Create', f'Created {interface.name}'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('interface.create'))
    return render_template('interface/create.html', form=form)


@blueprint.route('/read', methods=(('GET',)))
@auth.required
def read():
    name = request.args.get('name')
    interface = get_interface(name)
    if name and interface:
        update(interface)
        messages = [('Update', f'Using {interface.name}')]
        flash(tuple(messages), 'info')
        return redirect(url_for('interface.read'))
    return render_template('interface/read.html')


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
        return redirect(url_for('interface.delete'))
    return render_template('interface/delete.html')
