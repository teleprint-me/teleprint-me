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
from flask import url_for

from ledger.blueprints import auth

from ledger.forms.accounts import AccountsCreateForm

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


def get_accounts() -> list:
    """return a list of tuples containing a (<platform>, <key>) value pair"""
    return [(client.name, client.messenger.auth.token.key[:24]) for client in g.clients]


@bp.route('/menu', methods=('GET',))
@auth.required
def accounts_menu():
    return render_template('accounts/menu.html')


@bp.route("/create", methods=('GET', 'POST'))
@auth.required
def accounts_create():
    form = AccountsCreateForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            account = {
                'platform': form.platform.data,
                'key': form.key.data,
                'secret': form.secret.data
            }
            if form.platform.data == 'coinbase-pro':
                account.update({'passphrase': form.passphrase.data})
            result = g.db.accounts.insert_one(account)
            if result.acknowledged:
                messages.append(('Add', f'{account["platform"]} added successfully'))
            else:
                messages.append(('Failure', f'Oops! failed to add {account["platform"]}'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('accounts.accounts_create'))
    return render_template('accounts/create.html', form=form)


@bp.route('/view', methods=(('GET',)))
@auth.required
def accounts_view():
    accounts = get_accounts()
    return render_template('accounts/view.html', accounts=accounts)


@bp.route('/delete', methods=('GET', 'POST'))
@auth.required
def accounts_delete():
    platform = request.args.get('platform')
    account = g.db.accounts.find_one({'platform': platform})
    if account is not None:
        messages = [('Delete', f'{platform} deleted successfully')]
        g.db.accounts.delete_one(account)
        flash(tuple(messages), 'info')
        return redirect(url_for('accounts.accounts_delete'))
    accounts = get_accounts()
    return render_template('accounts/delete.html', accounts=accounts)
