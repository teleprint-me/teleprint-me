from logging import INFO, basicConfig, getLogger, handlers, info
from os import environ, path

instance_path = environ.get("INSTANCE_PATH", f'{environ.get("PWD")}/instance')
logging_path = path.join(instance_path, "teleprint-me.log")


def app(secret_key: bytes, sqlite: object):
    info(f"[app] [secret_key] {secret_key}")
    info(f"[app] [sqlite.instance_path] {sqlite.instance_path}")
    info(f"[app] [sqlite.database_path] {sqlite.database_path}")


def session(g: object):
    info(f"[session] [user] {g.user} [name] {g.user.name} [sid] {g.user.sid}")
    info(f"[session] [interface] {g.interface}")
    info(f"[session] [client] {g.client}")
    info(
        f"[session] [proxy] {g.proxy} [client] {g.proxy.client} [database] {g.proxy.database}"
    )


def session_error(g: object, error: object):
    info(f"[session] [user] {g.user} [error] {error}")


# level must be set to INFO
# if level is not set to INFO
# then log is flooded by werkzeug and flask
def initialize() -> handlers.RotatingFileHandler:
    basicConfig(
        filename=logging_path,
        filemode="w",
        level=INFO,
        format="%(levelname)s: %(message)s",
    )
    log = getLogger("teleprint-me")
    log.setLevel(INFO)
    handler = handlers.RotatingFileHandler(logging_path)
    log.addHandler(handler)
    return handler
