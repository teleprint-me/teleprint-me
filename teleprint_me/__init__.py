from datetime import datetime

from flask import Flask
from flask import render_template

from os import environ
from os import makedirs

from teleprint_me.core import generate
from teleprint_me.core import instance_path
from teleprint_me.core import database_path
from teleprint_me.core import database
from teleprint_me.core import init_database

from teleprint_me.blueprints import auth
from teleprint_me.blueprints import portfolio
# from teleprint_me.blueprints import proxy
# from teleprint_me.blueprints import settings
from teleprint_me.blueprints import interfaces
# from teleprint_me.blueprints import assets


def create_app() -> Flask:
    # Flask
    secret_key = environ.get('SECRET_KEY', generate.bytes())

    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True
    )

    app.config.from_mapping(SECRET_KEY=secret_key, DATABASE=database_path)

    # Database
    try:
        makedirs(instance_path)
    except (OSError,):
        pass

    init_database(database)

    @app.before_request
    def _db_connect():
        database.connect()

    @app.teardown_request
    def _db_close(exc):
        if not database.is_closed():
            database.close()

    # Blueprints
    @app.context_processor
    def utility_processor() -> dict:
        def timestamp() -> str:
            return datetime.now().isoformat()

        utils = {
            'zip': zip,
            'list': list,
            'timestamp': timestamp
        }

        return utils

    blueprints = (
        auth.blueprint,
        portfolio.blueprint,
        interfaces.blueprint
    )

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route('/menu')
    @auth.required
    def menu():
        return render_template('menu.html')

    @app.route('/license')
    @auth.required
    def license():
        return render_template('license.html')

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/menu', endpoint='menu')
    app.add_url_rule('/license', endpoint='license')

    return app
