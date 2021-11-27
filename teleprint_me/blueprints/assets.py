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
from ledger.blueprints.portfolio import get_client_context

from ledger.forms.assets import AssetsCreateForm

bp = Blueprint('assets', __name__, url_prefix='/assets')


@bp.route('/menu', methods=('GET',))
@auth.required
def assets_menu():
    return render_template('assets/menu.html')


@bp.route("/create", methods=('GET', 'POST'))
@auth.required
def assets_create():
    form = AssetsCreateForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            product = {
                'platform': form.platform.data,
                'asset': form.asset.data,
                'strategy': form.strategy.data,
                'principle': form.principle.data,
                'period': form.period.data,
                'apy': form.apy.data,
                'data': []
            }
            result = g.db.assets.insert_one(product)
            if result.acknowledged:
                messages.append(('Add', f'{product["asset"]} on {product["platform"]} added successfully'))
            else:
                messages.append(('Error', f'Oops! failed to add {product["asset"]}'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('assets.assets_create'))
    return render_template('assets/create.html', form=form)


@bp.route('/view', methods=(('GET',)))
@auth.required
def assets_view():
    assets = [asset for asset in g.db.assets.find()]
    return render_template('assets/view.html', assets=assets)


@bp.route('/delete', methods=('GET', 'POST'))
@auth.required
def assets_delete():
    product = g.db.assets.find_one({
        'platform': request.args.get('platform'),
        'asset': request.args.get('asset')
    })
    if product is not None:
        messages = [('Delete', f'{product["asset"]} on {product["platform"]} deleted successfully')]
        g.db.assets.delete_one(product)
        flash(tuple(messages), 'info')
        return redirect(url_for('assets.assets_delete'))
    assets = [asset for asset in g.db.assets.find()]
    return render_template('assets/delete.html', assets=assets)


@bp.route('/trade', methods=('GET', 'POST'))
@auth.required
def assets_trade():
    context = [{'platform': client.name, 'assets': client.get_assets()} for client in g.clients]
    products = [product for product in g.db.assets.find()]
    if request.method == "POST":
        pass
    return render_template('assets/trade.html', context=context, assets=products)


@bp.route('/trade/<asset>', methods=('GET', 'POST'))
@auth.required
def assets_trade_product(asset):
    if request.method == 'POST':
        pass
    return {'asset', asset}
