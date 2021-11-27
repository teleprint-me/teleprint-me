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
from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from ledger.core import mongo
from ledger.blueprints import auth
from ledger.forms.settings import SettingsUpdateForm

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route("/update", methods=('GET', 'POST'))
@auth.required
def settings_update():
    form = SettingsUpdateForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            settings = {
                '$set': {
                    'currency': form.currency.data,
                    'theme': form.theme.data,
                    '2fa': form.tfa.data
                }
            }
            result = mongo.cx.ledger.users.update_one(g.user, settings)
            if result.acknowledged:
                messages.append(('Update', 'Settings updated successfully'))
            else:
                messages.append(('Error', 'Oops! failed to update settings'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('settings.settings_update'))
    return render_template('settings.html', form=form)


@bp.route('/delete', methods=('GET',))
@auth.required
def settings_delete():
    email = request.args.get('email')
    database = request.args.get('database')
    if email == g.user['email'] and database == str(g.user['database']):
        mongo.db.users.delete_one(g.user)
        mongo.cx.drop_database(g.db)
        session.clear()
        redirect(url_for('auth.sign_in'))
    return redirect(url_for('settings.settings_update'))
