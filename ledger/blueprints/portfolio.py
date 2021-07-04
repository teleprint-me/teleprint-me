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
from flask import g
from flask import render_template
from flask import Blueprint

from ledger.blueprints import auth

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET',))
@auth.required
def portfolio():
    assets = []
    for client in g.accounts:
        for asset in client.get_accounts():
            if float(asset['balance']) > 0:
                asset.update({'account': client.name})
                assets.append(asset)
    return render_template('portfolio.html', assets=assets)
