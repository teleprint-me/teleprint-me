from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from teleprint_me.blueprints import auth
from teleprint_me.core import sqlite
from teleprint_me.forms.interface import InterfaceForm

blueprint = Blueprint("interface", __name__, url_prefix="/interface")


@blueprint.route("/menu", methods=("GET",))
@auth.required
def menu():
    return render_template("interface/menu.html")


@blueprint.route("/read", methods=("GET",))
@auth.required
def read():
    return render_template("interface/read.html", action="read")


@blueprint.route("/read/<name>", methods=(("GET",)))
@auth.required
def read_one(name):
    interface = g.proxy.database.interface.get(name)
    if interface:
        sqlite.set_interface_active(g.user, interface)
        flash((("Read", f"Reading {interface.name}"),), "info")
        return redirect(url_for("interface.read"))
    return render_template("interface/read.html", action="read")


@blueprint.route("/delete", methods=("GET", "POST"))
@auth.required
def delete():
    return render_template("interface/read.html", action="delete")


@blueprint.route("/delete/<name>", methods=("GET", "POST"))
@auth.required
def delete_one(name):
    interface = g.proxy.database.interface.get(name)
    if name and interface:
        if interface.active:
            messages = (("Delete", f"Deleted active {interface.name}"),)
        else:
            messages = (("Delete", f"Deleted inactive {interface.name}"),)
        interface.delete_instance()
        flash(messages, "info")
        return redirect(url_for("interface.delete"))
    return render_template("interface/delete.html")


@blueprint.route("/create", methods=("GET", "POST"))
@auth.required
def create():
    form = InterfaceForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            interface = sqlite.Interface.create(
                name=form.name.data,
                key=form.key.data,
                secret=form.secret.data,
                passphrase=form.passphrase.data,
                rest=form.rest.data,
                feed=form.feed.data,
                active=form.active.data,
                user=g.user,
            )
            g.proxy.database.interface.set_active(g.user, interface)
            messages.append(("Create", f"Created {interface.name}"))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(("Error", e))
        if messages:
            flash(tuple(messages), "info")
        return redirect(url_for("interface.create"))
    return render_template("interface/create.html", form=form)
