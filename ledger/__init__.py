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
from ledger.core import mongo

from ledger.blueprints import auth
from ledger.blueprints import proxy
from ledger.blueprints import settings
from ledger.blueprints import accounts
from ledger.blueprints import assets
from ledger.blueprints import portfolio

from flask import Flask
from flask import render_template

import datetime


blueprints = (
    auth.bp,
    proxy.bp,
    settings.bp,
    accounts.bp,
    assets.bp,
    portfolio.bp
)


def get_config(config: str) -> str:
    if not config:
        return 'ledger.core.config'
    return config


def define_utility_processor(app: Flask) -> Flask:
    @app.context_processor
    def utility_processor() -> dict:
        def timestamp() -> str:
            return datetime.datetime.now().isoformat()

        utils = {
            'zip': zip,
            'list': list,
            'timestamp': timestamp
        }

        return utils
    return app


def create_app(config: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    config = get_config(config)
    app.config.from_object(config)
    app = define_utility_processor(app)
    mongo.init_app(app)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.route('/menu.html')
    @auth.required
    def menu():
        return render_template('menu.html')

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/menu', endpoint='menu')
    return app
