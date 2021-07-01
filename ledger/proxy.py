from ledger import auth

import flask


bp = flask.Blueprint('proxy', __name__, url_prefix='/client')


@bp.route('/platforms', methods=('GET',))
@auth.required
def proxy_platforms():
    accounts = list()
    for account in flask.g.accounts:
        accounts.append(account.name)
    return flask.jsonify(accounts)


@bp.route('/<platform>/assets', methods=('GET',))
@auth.required
def proxy_assets(platform):
    assets = list()
    for account in flask.g.accounts:
        if account.name == platform:
            assets = account.get_assets()
            break
    return flask.jsonify(assets)


@bp.route('/<platform>/accounts', methods=('GET',))
@auth.required
def proxy_accounts(platform):
    accounts = list()
    for account in flask.g.accounts:
        if account.name == platform:
            accounts = account.get_accounts()
            break
    return flask.jsonify(accounts)


@bp.route('/<platform>/history/<asset>', methods=('GET',))
@auth.required
def proxy_history(platform, asset):
    history = list()
    for account in flask.g.accounts:
        if account.name == platform:
            history = account.get_history(asset)
            break
    return flask.jsonify(history)


@bp.route('/<platform>/price/<asset>', methods=('GET',))
@auth.required
def proxy_price(platform, asset):
    price = dict()
    for account in flask.g.accounts:
        if account.name == platform:
            price = account.get_price(asset)
            break
    return flask.jsonify(price)


@bp.route('/<platform>/order', methods=('POST',))
@auth.required
def proxy_order(platform):
    pass
