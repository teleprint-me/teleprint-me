from flask import g
from flask import jsonify
from flask import Blueprint

from teleprint_me.blueprints import auth

blueprint = Blueprint('client', __name__, url_prefix='/client')


@blueprint.route('/name', methods=('GET',))
@auth.required
def label():
    return jsonify({'client': g.client.label()})


@blueprint.route('/time', methods=('GET',))
@auth.required
def time_get():
    return jsonify(g.client.time.get())


@blueprint.route('/currency/list', methods=('GET',))
@auth.required
def currency_list():
    return jsonify(g.client.currency.list())


@blueprint.route('/currency/get/<currency_id>', methods=('GET',))
@auth.required
def currency_get(currency_id):
    return jsonify(g.client.currency.get(currency_id))


@blueprint.route('/product/list', methods=('GET',))
@auth.required
def product_list():
    return jsonify(g.client.product.list())


@blueprint.route('/product/list/ids', methods=('GET',))
@auth.required
def product_list_ids():
    return jsonify([product['id'] for product in g.client.product.list()])


@blueprint.route('/product/ticker/<product_id>', methods=('GET',))
@auth.required
def product_ticker(product_id):
    return jsonify(g.client.product.ticker(product_id))


@blueprint.route('/account/list', methods=('GET',))
@auth.required
def account_list():
    return jsonify(g.client.account.list())


@blueprint.route('/order/fills/<product_id>', methods=('GET',))
@auth.required
def order_fills(product_id):
    return jsonify(g.client.order.fills({'product_id': product_id}))


@blueprint.route('/order/<product_id>', methods=('POST',))
@auth.required
def order_post(product_id):
    return jsonify({})


@blueprint.route('/transfer/list', methods=('GET',))
@auth.required
def transfer_list():
    return jsonify(g.client.transfer.list())


@blueprint.route('/deposits/<product_id>', methods=('GET',))
@auth.required
def transfer_list_deposits(product_id):
    return jsonify({})


@blueprint.route('/withdrawals/<product_id>', methods=('GET',))
@auth.required
def transfer_list_withdrawals(product_id):
    return jsonify({})
