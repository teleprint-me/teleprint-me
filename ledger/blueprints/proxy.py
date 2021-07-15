from flask import g
from flask import jsonify
from flask import Blueprint

from ledger.blueprints import auth

bp = Blueprint('proxy', __name__, url_prefix='/client')


@bp.route('/platforms', methods=('GET',))
@auth.required
def proxy_client_names():
    names = list()
    for client in g.clients:
        names.append(client.name)
    return jsonify(names)


@bp.route('/<platform>/assets', methods=('GET',))
@auth.required
def proxy_assets(platform):
    for client in g.clients:
        if client.name == platform:
            return jsonify(client.get_assets())
    return jsonify([])


@bp.route('/<platform>/accounts', methods=('GET',))
@auth.required
def proxy_accounts(platform):
    for client in g.clients:
        if client.name == platform:
            return jsonify(client.get_accounts())
    return jsonify([])


@bp.route('/<platform>/history/<asset>', methods=('GET',))
@auth.required
def proxy_history(platform, asset):
    for client in g.clients:
        if client.name == platform:
            return jsonify(client.get_history(asset))
    return jsonify([])


@bp.route('/<platform>/price/<asset>', methods=('GET',))
@auth.required
def proxy_price(platform, asset):
    for client in g.clients:
        if client.name == platform:
            return jsonify(client.get_price(asset))
    return jsonify({})


@bp.route('/<platform>/order/<asset>', methods=('POST',))
@auth.required
def proxy_order(platform, asset):
    pass
