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

from ledger.blueprints import auth

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


def get_accounts() -> list:
    """return a list of tuples containing a (<platform>, <key>) value pair"""
    keys = list()
    accounts = [account for account in g.db.accounts.find()]
    for account in accounts:
        platform = account['platform']
        key = account['key'][:32]
        keys.append((platform, key))
    return keys


@bp.route('/menu', methods=('GET',))
@auth.required
def accounts_menu():
    return render_template('accounts/menu.html')


@bp.route("/create", methods=('GET', 'POST'))
@auth.required
def accounts_create():
    if request.method == "POST":
        message = None

        account = {
            'platform': request.form.get('platform'),
            'key': request.form.get('key'),
            'secret': request.form.get('secret')
        }

        if not account['platform']:
            message = 'Error', 'Please select a valid platform'

        if account['platform'] == 'coinbase-pro':
            account.update({'passphrase': request.form.get('passphrase')})

        if not account['key']:
            message = 'Error', 'A API Key is required'

        if not account['secret']:
            message = 'Error', 'A API Secret is required'

        if account['platform'] == 'coinbase-pro' and not account['passphrase']:
            message = 'Error', 'A API Passphrase is required'

        document = g.db.accounts.find_one({'platform': account['platform']})
        if document:
            message = 'Error', f'{account["platform"]} already exists'

        if message is None:
            result = g.db.accounts.insert_one(account)
            if result.acknowledged:
                message = 'Success', f'{account["platform"]} account added successfully'
            else:
                message = 'Error', f'Oops! failed to add {account["platform"]}'

        flash(message)

    return render_template('accounts/create.html')


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
        g.db.accounts.delete_one(account)
        flash((f'Delete', f'{platform} was deleted successfully'))
    accounts = get_accounts()
    return render_template('accounts/delete.html', accounts=accounts)
