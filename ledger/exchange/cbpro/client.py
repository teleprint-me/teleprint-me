# Ledger - A web application to track cryptocurrency investments
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from ledger.exchange.factory import AbstractMessenger
from ledger.exchange.factory import AbstractClient
from ledger.exchange.factory import AbstractFactory

from ledger.exchange.cbpro.auth import Auth
from ledger.exchange.cbpro.messenger import Messenger


class CoinbaseProClient(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__name = 'coinbase-pro'
        self.__messenger = messenger

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def has_error(self, response: object) -> bool:
        if isinstance(response, dict):
            return bool(response.get('message'))
        return False

    def get_assets(self) -> list:
        assets = list()
        response = self.messenger.get('/products')
        if self.has_error(response):
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
        response = self.messenger.get('/accounts')
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
        response = self.messenger.paginate('/fills', {'product_id': asset})
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
        response = self.messenger.get(f'/products/{asset}/ticker')
        if self.has_error(response):
            return response
        return {
            'bid': response['bid'],
            'ask': response['ask'],
            'price': response['price']
        }

    def post_order(self, data: dict) -> dict:
        # TODO: Filter out redundent data
        response = self.messenger.post('/orders', data)
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
    def get_client(self,
                   key: str,
                   secret: str,
                   passphrase: str) -> AbstractClient:

        auth = Auth(key, secret, passphrase)
        messenger = Messenger(auth)
        return CoinbaseProClient(messenger)
