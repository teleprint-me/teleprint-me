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
from flask import Flask

from ledger.core.extensions import mongo

from ledger import portfolio
from ledger import accounts
from ledger import assets
from ledger import auth


def create_app(config: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        config = 'ledger.core.config'

    app.config.from_object(config)

    mongo.init_app(app)

    @app.context_processor
    def utility_processor():
        def timestamp():
            import datetime
            date, time = datetime.datetime.now().isoformat().split('T')
            time = time.split('.')[0]
            return f'{date}@{time}'

        utils = {
            'zip': zip,
            'list': list,
            'timestamp': timestamp
        }

        return utils

    app.register_blueprint(auth.bp)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(assets.bp)

    app.add_url_rule('/', endpoint='index')

    return app
