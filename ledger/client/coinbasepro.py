from ledger.client.factory import AbstractClient
from ledger.client.factory import AbstractFactory

import cbpro


class CoinbaseProClient(AbstractClient):
    def __init__(self, client: cbpro.PrivateClient):
        self.__name = 'coinbase-pro'
        self.__client = client

    @property
    def name(self) -> str:
        return self.__name

    @property
    def client(self) -> cbpro.PrivateClient:
        return self.__client

    def has_error(self, response: object) -> bool:
        return bool(response.get('message'))

    def get_assets(self) -> list:
        assets = list()
        response = self.client.products.list()
        if 'message' in response:
            return response
        for item in response:
            assets.append({
                'id': item['id'],
                'display': item['display_name'],
                'name': item['base_currency'],
                'min-size': item['min_market_funds']
            })
        return assets

    def get_accounts(self) -> list:
        accounts = list()
        response = self.client.accounts.list()
        if self.has_error(response):
            return response
        for item in response:
            accounts.append({
                'name': item['currency'],
                'balance': item['available']
            })
        return accounts

    def get_history(self, asset: str) -> list:
        fills = list()
        response = self.client.fills.list({'product_id': asset})
        if self.has_error(response):
            return response
        for fill in response:
            fills.append({
                'timestamp': fill['created_at'],
                'id': fill['product_id'],
                'side': fill['side'],
                'price': fill['price'],
                'size': fill['size']
            })
        return fills

    def get_price(self, asset: str) -> dict:
        response = self.client.products.ticker(asset)
        if self.has_error(response):
            return response
        return {
            'bid': response['bid'],
            'ask': response['ask'],
            'price': response['price']
        }

    def post_order(self, data: dict) -> dict:
        # TODO: Filter out redundent data
        response = self.client.orders.post(data)
        if self.has_error(response):
            return response
        return {
            'timestamp': response['created_at'],
            'id': response['product_id'],
            'side': response['side'],
            'price': response['price'],
            'size': response['size']
        }


class CoinbaseProFactory(AbstractFactory):
    def get_client(self, key: str, secret: str, passphrase: str) -> AbstractClient:
        client = cbpro.private_client(key, secret, passphrase)
        return CoinbaseProClient(client)
