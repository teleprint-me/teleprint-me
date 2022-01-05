from coinbase_pro.client import Client


def get_account(client: Client, product_id: str) -> dict:
    accounts = client.account.list()
    for account in accounts:
        if account['currency'] == product_id.split('-')[0]:
            return account
    return {}


def get_transfers(client: Client, tx_type: str, account: dict) -> list[dict]:
    transfers = []
    txs = client.transfer.list()
    for tx in txs:
        if tx['type'] == tx_type:
            if account['id'] == tx['account_id']:
                transfers.append(tx)
    return transfers


def get_withdrawals(client: Client, product_id: str) -> list[dict, list[dict]]:
    account = get_account(client, product_id)
    withdrawals = get_transfers(client, 'withdraw', account)
    return [account, withdrawals]


def get_deposits(client: Client, product_id: str) -> list[dict, list[dict]]:
    account = get_account(client, product_id)
    deposits = get_transfers(client, 'deposit', account)
    return [account, deposits]


def get_fills(client: Client, product_id: str) -> list[dict]:
    return client.order.fills({'product_id': product_id})


def get_price(client: Client, product_id: str) -> dict:
    return client.product.ticker(product_id)


def get_order(client: Client, data: dict) -> dict:
    return client.order.post(data)


def post_order():
    pass
