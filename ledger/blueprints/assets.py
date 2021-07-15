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

bp = Blueprint('assets', __name__, url_prefix='/assets')


def get_account_options() -> list:
    options = []
    for client in g.clients:
        inner_text = ' '.join(word.capitalize() for word in client.name.split('-'))
        options.append({'value': client.name, 'inner-text': inner_text})
    return options


def get_asset_options() -> list:
    options = []
    for client in g.clients:
        assets = client.get_assets()
        if assets:
            options.append({'platform': client.name, 'assets': assets})
    return options


@bp.route('/menu', methods=('GET',))
@auth.required
def assets_menu():
    return render_template('assets/menu.html')


@bp.route("/create", methods=('GET', 'POST'))
@auth.required
def assets_create():
    g.data = {
        'accounts': get_account_options(),
        'assets': get_asset_options()
    }

    if request.method == "POST":
        message = None

        # get the form fields
        account = request.form.get('account')
        asset = request.form.get('asset')
        strategy = request.form.get('strategy')
        principle = request.form.get('principle')
        period = request.form.get('period')
        apy = request.form.get('apy')

        # check the form fields
        if not account:
            message = 'Error', '`Account` is required'
        elif not asset:
            message = 'Error', '`Asset Pair` is required'
        elif not strategy:
            message = 'Error', '`Strategy` is required'
        elif not principle:
            message = 'Error', '`Principle Amount` is required'
        elif not apy:
            message = 'Error', '`Annual Percentage Yield` is required'

        # check to see if the record already exists
        record = g.db.assets.find_one({'account': account, 'asset': asset})
        if record:
            message = 'Error', f'{account} and {asset} pair already exists!'

        # insert the document into the database
        if not message:
            result = g.db.assets.insert_one({
                'ledger': [],
                'account': account,
                'asset': asset,
                'strategy': strategy,
                'principle': principle,
                'period': period,
                'apy': apy
            })
            if result.acknowledged:
                message = 'Info', f'Created {asset} pair using {strategy}'
            else:
                message = 'Error', f'Failed to create {asset} pair using {strategy}'

        flash(message, message[0].lower())

    return render_template('assets/create.html')


@bp.route('/view', methods=(('GET',)))
@auth.required
def assets_view():
    assets = [asset for asset in g.db.assets.find()]
    return render_template('assets/view.html', assets=assets)


@bp.route('/delete', methods=('GET', 'POST'))
@auth.required
def assets_delete():
    platform = request.args.get('platform')
    account = g.db.accounts.find_one({'platform': platform})
    if account is not None:
        g.db.accounts.delete_one(account)
        flash(('Delete', f'{platform} was deleted successfully'))
    return render_template('assets/delete.html')
