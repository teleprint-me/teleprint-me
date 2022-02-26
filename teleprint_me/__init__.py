from os import environ, makedirs

from flask import Flask, render_template

from teleprint_me.blueprints import (
    auth,
    client,
    interface,
    portfolio,
    setting,
    strategy,
)
from teleprint_me.core import generate, log, sqlite, timestamp


def create_app() -> Flask:
    # instance
    try:
        makedirs(sqlite.instance_path)
    except (OSError,):
        pass

    # app
    secret_key = environ.get("SECRET_KEY", generate.bytes())

    app = Flask(
        __name__, instance_path=sqlite.instance_path, instance_relative_config=True
    )

    # log
    handler = log.initialize()
    app.logger.addHandler(handler)
    log.app(secret_key, sqlite)

    app.config.from_mapping(SECRET_KEY=secret_key, DATABASE=sqlite.database_path)

    # database
    sqlite.initialize()

    @app.before_request
    def db_connect():
        sqlite.database.connect()

    @app.teardown_request
    def db_close(exc):
        if not sqlite.database.is_closed():
            sqlite.database.close()

    # blueprints
    @app.context_processor
    def utility_processor() -> dict:
        return {
            "zip": zip,
            "list": list,
            "sqlite": sqlite,
            "timestamp": timestamp,
        }

    blueprints = (
        auth.blueprint,
        interface.blueprint,
        strategy.blueprint,
        setting.blueprint,
        client.blueprint,
        portfolio.blueprint,
    )

    for bp in blueprints:
        app.register_blueprint(bp)

    # routes
    @app.route("/menu")
    @auth.required
    def menu():
        return render_template("menu.html")

    @app.route("/license")
    @auth.required
    def license_():
        return render_template("license.html")

    # rules
    app.add_url_rule("/", endpoint="index")
    app.add_url_rule("/menu", endpoint="menu")
    app.add_url_rule("/license", endpoint="license")

    return app
