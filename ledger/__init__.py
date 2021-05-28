from flask import Flask

from ledger.core.extensions import mongo

from ledger import index
from ledger import auth


def create_app(config: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        config = 'ledger.core.config'

    app.config.from_object(config)

    mongo.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)

    app.add_url_rule("/", endpoint="index")

    return app
