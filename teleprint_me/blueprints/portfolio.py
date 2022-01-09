from flask import Blueprint, g, render_template
from teleprint_me.blueprints import auth

blueprint = Blueprint("index", __name__)


def get_accounts() -> list[dict]:
    accounts = g.client.account.list()
    if "message" in accounts:
        return [accounts]
    return [account for account in accounts if 0 < float(account["balance"])]


def get_products(accounts: list[dict]) -> list[dict]:
    data = []
    products = g.client.product.list()
    if "message" in products:
        return [products]
    for account in accounts:
        for product in products:
            product_id = product.get("id")
            target_id = f'{account.get("currency")}-{g.user.currency}'
            if product_id == target_id:
                data.append(product)
    return data


def get_product_ids(products: list[dict]) -> list[str]:
    return [product["id"] for product in products]


def get_context() -> dict:
    accounts = get_accounts()
    products = get_products(accounts)
    product_ids = get_product_ids(products)
    return {
        "name": g.client.name,
        "feed": g.interface.feed,
        "accounts": accounts,
        "products": products,
        "product_ids": product_ids,
    }


@blueprint.route("/", methods=("GET",))
@auth.required
def portfolio():
    try:
        context = get_context()
    except (AttributeError,):
        context = {}
    return render_template("portfolio.html", context=context)
