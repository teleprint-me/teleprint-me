from flask import Blueprint, g, jsonify
from teleprint_me.blueprints import auth
from teleprint_me.core import sqlite

blueprint = Blueprint("client", __name__, url_prefix="/client")


#
# Client
#
@blueprint.route("/name", methods=("GET",))
@auth.required
def get_name():
    return jsonify({"client": g.client.name})


@blueprint.route("/time", methods=("GET",))
@auth.required
def get_time():
    return jsonify(g.client.time.get())


#
# Product
#
@blueprint.route("/product", methods=("GET",))
@auth.required
def get_product_list():
    return jsonify(g.client.product.list())


@blueprint.route("/product/id", methods=("GET",))
@auth.required
def get_product_id_list():
    return jsonify(g.proxy.get_product_ids(g.client))


@blueprint.route("/product/<product_id>", methods=("GET",))
@auth.required
def get_product(product_id):
    return jsonify(g.client.product.get(product_id.upper()))


@blueprint.route("/product/ticker/<product_id>", methods=("GET",))
@auth.required
def get_product_ticker(product_id):
    return jsonify(g.client.product.ticker(product_id.upper()))


#
# Currency
#
@blueprint.route("/currency", methods=("GET",))
@auth.required
def get_currency_list():
    return jsonify(g.client.currency.list())


@blueprint.route("/currency/<currency_id>", methods=("GET",))
@auth.required
def get_currency(currency_id):
    return jsonify(g.client.currency.get(currency_id.upper()))


#
# Account
#
@blueprint.route("/account", methods=("GET",))
@auth.required
def get_account_list():
    return jsonify(g.client.account.list())


@blueprint.route("/account/<currency_id>", methods=("GET",))
@auth.required
def get_account(currency_id):
    return jsonify(g.proxy.get_account(g.client, currency_id.upper()))


#
# Transfer
#
@blueprint.route("/transfer", methods=("GET",))
@auth.required
def get_transfer_list():
    return jsonify(g.client.transfer.list())


@blueprint.route("/transfer/<currency_id>", methods=("GET",))
@auth.required
def get_transfer_filter(currency_id):
    return jsonify(g.proxy.get_transfers(g.client, currency_id.upper()))


@blueprint.route("/transfer/deposit/<currency_id>", methods=("GET",))
@auth.required
def get_deposit_filter(currency_id):
    return jsonify(g.proxy.get_deposits(g.client, currency_id.upper()))


@blueprint.route("/transfer/withdraw/<currency_id>", methods=("GET",))
@auth.required
def get_withdraw_filter(currency_id):
    return jsonify(g.proxy.get_withdrawals(g.client, currency_id.upper()))


#
# Order
#
@blueprint.route("/order/fill/<product_id>", methods=("GET",))
@auth.required
def get_order_fill_list(product_id):
    return jsonify(g.proxy.get_fills(g.client, product_id.upper()))


@blueprint.route("/order/<product_id>", methods=("POST",))
@auth.required
def post_order(product_id):
    return jsonify({})


#
# User
#
@blueprint.route("/user", methods=("GET",))
@auth.required
def get_user():
    return jsonify(sqlite.user_to_dict(g.user))


#
# Interface
#
@blueprint.route("/interface", methods=("GET",))
@auth.required
def get_interface_list():
    return jsonify(sqlite.get_interface_list(g.user))


@blueprint.route("/interface/active", methods=("GET",))
@auth.required
def get_interface_active():
    interface = sqlite.get_interface_active(g.user.interfaces)
    interface_dict = sqlite.interface_to_dict(interface)
    return jsonify(interface_dict)


@blueprint.route("/interface/<name>", methods=("GET",))
@auth.required
def get_interface(name):
    interface = sqlite.get_interface(name)
    interface_dict = sqlite.interface_to_dict(interface)
    return jsonify(interface_dict)


#
# Strategy
#
@blueprint.route("/strategy", methods=("GET",))
@auth.required
def get_strategy_list():
    return jsonify(sqlite.get_strategy_list(g.user))


@blueprint.route("/strategy/<name>", methods=("GET",))
@auth.required
def get_strategy(name):
    strategy = sqlite.get_strategy(name)
    strategy_dict = sqlite.strategy_to_dict(strategy)
    return jsonify(strategy_dict)


#
# Data
#
@blueprint.route("/strategy/<name>/datum", methods=("GET",))
@auth.required
def get_strategy_data_list(name):
    strategy = sqlite.get_strategy(name)
    strategy_list = sqlite.get_data_list(strategy)
    return jsonify(strategy_list)


@blueprint.route("/strategy/<name>/data", methods=("GET",))
@auth.required
def get_strategy_data(name):
    strategy = sqlite.get_strategy(name)
    strategy_dict = sqlite.data_to_dict(strategy)
    return jsonify(strategy_dict)
