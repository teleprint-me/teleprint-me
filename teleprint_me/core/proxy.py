from coinbase_pro.client import CoinbasePro


#
# Account
#
def filter_accounts(client: CoinbasePro, floor: float = None) -> list[dict]:
    floor = float(floor) if floor else 0.0
    return [a for a in client.account.list() if floor < float(a.get("balance", 0))]


def get_account(client: CoinbasePro, currency: str) -> dict:
    try:
        return [a for a in client.account.list() if a.get("currency") == currency][0]
    except (IndexError,):
        return {}


#
# Transfer
#
def filter_transactions(client: CoinbasePro, account: dict, tx_type: str) -> list[dict]:
    txs = client.transfer.list()
    return [
        tx
        for tx in txs
        if account.get("id") == tx.get("account_id") and tx.get("type") == tx_type
    ]


def filter_transfers(client: CoinbasePro, account: dict) -> list[dict]:
    txs = client.transfer.list()
    return [tx for tx in txs if account.get("id") == tx.get("account_id")]


def get_transfers(client: CoinbasePro, currency: str) -> list[dict, list[dict]]:
    account = get_account(client, currency)
    txs = filter_transfers(client, account)
    return [account, txs]


def get_withdrawals(client: CoinbasePro, currency: str) -> list[dict, list[dict]]:
    account = get_account(client, currency)
    withdrawals = filter_transactions(client, account, "withdraw")
    return [account, withdrawals]


def get_deposits(client: CoinbasePro, currency: str) -> list[dict, list[dict]]:
    account = get_account(client, currency)
    deposits = filter_transactions(client, account, "deposit")
    return [account, deposits]


#
# Product
#
def get_product_ids(client: CoinbasePro) -> list[str]:
    return [product.get("id") for product in client.product.list()]


def get_price(client: CoinbasePro, product_id: str) -> dict:
    return client.product.ticker(product_id)


#
# Order
#
def get_fills(client: CoinbasePro, product_id: str) -> list[dict]:
    return client.order.fills({"product_id": product_id})


def get_order():
    pass


def post_order(client: CoinbasePro, data: dict) -> dict:
    return client.order.post(data)
