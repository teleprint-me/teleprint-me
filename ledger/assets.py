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

from ledger import auth

bp = Blueprint('assets', __name__, url_prefix='/assets')


def get_account_options() -> list:
    options = []
    for account in g.accounts:
        value = account['platform']
        inner_text = ' '.join(word.capitalize() for word in value.split('-'))
        options.append({'value': value, 'inner-text': inner_text})
    return options


def get_asset_options() -> list:
    options = []
    for account in g.accounts:
        platform = account['platform']
        client = account['client']
        if platform == 'coinbase-pro':
            assets = client.products.list()
        if platform == 'kraken':
            assets = client.market.pairs()['result']
        options.append({'platform': platform, 'assets': assets})
    return options


@bp.route('/menu', methods=('GET',))
@auth.required
def assets_menu():
    return render_template('assets/menu.html')


@bp.route("/create", methods=('GET', 'POST'))
@auth.required
def assets_create():
    # assets need to be serialized so that javascript can access
    # the data. this should only be done with trusted 3rd party data.
    # doing otherwise will lead to xss vulnerabilities.
    g.data = {
        'accounts': get_account_options(),
        'assets': get_asset_options()
    }

    if request.method == "POST":
        meta, data, message = None, None, None
        account = request.form.get('account'),
        asset = request.form.get('asset'),
        strategy = request.form.get('strategy'),
        principle = request.form.get('principle'),
        period = request.form.get('period'),
        apy = request.form.get('apy')

        record = g.db.assets.find_one({
            'meta': {
                'account': account, 'asset': asset
            }
        })

        if record:
            message = 'Error', f'{account} and {asset} pair already exists!'
        elif account == 'coinbase-pro':
            pass
        elif account == 'kraken':
            pass
        else:
            message = 'Error', f'Got {asset} with {strategy}'

        if not message:
            g.db.assets.insert_one()

        flash(message, message[0].lower())

    return render_template('assets/create.html')


@bp.route('/view', methods=(('GET',)))
@auth.required
def assets_view():
    accounts = [account for account in g.db.accounts.find()]
    for account in accounts:
        if account['platform'] == 'coinbase-pro':
            pass
        elif account['platform'] == 'kraken':
            pass
        else:
            break
    return render_template('assets/view.html')


@bp.route('/delete', methods=('GET', 'POST'))
@auth.required
def assets_delete():
    platform = request.args.get('platform')
    account = g.db.accounts.find_one({'platform': platform})
    if account is not None:
        g.db.accounts.delete_one(account)
        flash((f'Delete', f'{platform} was deleted successfully'))
    return render_template('assets/delete.html')
