from flask import g
from flask import jsonify
from flask import Blueprint

from ledger.blueprints import auth

bp = Blueprint('proxy', __name__, url_prefix='/client')


@bp.route('/platforms', methods=('GET',))
@auth.required
def proxy_platforms():
    accounts = list()
    for account in g.accounts:
        accounts.append(account.name)
    return jsonify(accounts)


@bp.route('/<platform>/assets', methods=('GET',))
@auth.required
def proxy_assets(platform):
    assets = list()
    for account in g.accounts:
        if account.name == platform:
            assets = account.get_assets()
            break
    return jsonify(assets)


@bp.route('/<platform>/accounts', methods=('GET',))
@auth.required
def proxy_accounts(platform):
    accounts = list()
    for account in g.accounts:
        if account.name == platform:
            accounts = account.get_accounts()
            break
    return jsonify(accounts)


@bp.route('/<platform>/history/<asset>', methods=('GET',))
@auth.required
def proxy_history(platform, asset):
    history = list()
    for account in g.accounts:
        if account.name == platform:
            history = account.get_history(asset)
            break
    return jsonify(history)


@bp.route('/<platform>/price/<asset>', methods=('GET',))
@auth.required
def proxy_price(platform, asset):
    price = dict()
    for account in g.accounts:
        if account.name == platform:
            price = account.get_price(asset)
            break
    return jsonify(price)


@bp.route('/<platform>/order', methods=('POST',))
@auth.required
def proxy_order(platform):
    pass
