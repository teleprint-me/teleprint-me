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
from ledger.exchange.factory import AbstractContext
from ledger.exchange.factory import AbstractClient
from ledger.exchange.factory import AbstractFactory

from ledger.exchange.kraken.auth import Auth
from ledger.exchange.kraken.messenger import Messenger

from time import sleep
from datetime import datetime


def on_error(response: object) -> bool:
    return bool(response.get('error'))


def epoch_to_datetime(timestamp: float) -> str:
    '''convert timestamp from epoch to iso 8601'''
    date = datetime.fromtimestamp(timestamp)
    return date.isoformat()


def get_average_price(prices: list) -> str:
    '''return average price based on approx bids and asks at market value'''
    pricelist = sum(float(p) for p in prices) / len(prices)
    return f'{pricelist:.5f}'


def get_history(asset: str, response: object) -> object:
    for trade in response['result']['trades'].values():
        if trade['pair'] == asset:
            yield {
                'id': trade['pair'],
                'side': trade['type'],
                'price': trade['price'],
                'size': trade['vol'],
                'timestamp': epoch_to_datetime(trade['time'])
            }


def get_transfers(asset: str, response: object) -> object:
    for transfer in response['result']['ledger'].values():
        if asset == 'all' or transfer['asset'] == asset.split('Z')[0]:
            yield {
                'type': transfer['type'],
                'currency': transfer['asset'],
                'amount': transfer['amount'],
                'fee': transfer['fee'],
                'timestamp': epoch_to_datetime(transfer['time'])
            }


class Context(AbstractContext):
    def __init__(self, endpoint: str, params: dict = None):
        self.__endpoint = endpoint
        self.__params = {} if params is None else params
        self.__asset = ''
        self.__callback = lambda default: None

    @property
    def endpoint(self) -> str:
        return self.__endpoint

    @property
    def params(self) -> dict:
        return self.__params

    @property
    def asset(self) -> str:
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value

    @property
    def callback(self) -> object:
        return self.__callback

    @callback.setter
    def callback(self, value: object):
        self.__callback = value


class KrakenClient(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__name = 'kraken'
        self.__messenger = messenger

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def get_assets(self) -> list:
        response = self.messenger.get('/public/AssetPairs')
        if on_error(response):
            return response['error']
        return [{
                'id': k,
                'display': v.get('wsname'),
                'name': v.get('base'),
                'min-size': v.get('ordermin')
                } for k, v in response['result'].items()]

    def get_accounts(self) -> list:
        response = self.messenger.post('/private/Balance')
        if on_error(response):
            return response['error']
        return [{
                'name': k,
                'balance': v
                } for k, v in response['result'].items() if float(v) > 0]

    def get_history(self, asset: str) -> list:
        context = Context('/private/TradesHistory')
        context.asset = asset
        context.callback = get_history
        return self.messenger.page(context)

    def get_deposits(self, asset: str) -> list:
        context = Context('/private/Ledgers', {'type': 'deposit'})
        context.asset = asset
        context.callback = get_transfers
        return self.messenger.page(context)

    def get_withdrawals(self, asset: str) -> list:
        context = Context('/private/Ledgers', {'type': 'withdrawal'})
        context.asset = asset
        context.callback = get_transfers
        return self.messenger.page(context)

    def get_price(self, asset: str) -> dict:
        response = self.messenger.get('/public/Ticker', {'pair': asset})
        if self.has_error(response):
            return response['error']
        ticker = response['result'][asset]
        return {
            'bid': ticker['b'][0],
            'ask': ticker['a'][0],
            'price': get_average_price(ticker['p'])
        }

    def post_order(self, data: dict) -> dict:
        order = self.messenger.post('/private/AddOrder', data)
        if self.has_error(order):
            return order['error']
        txid = order['result']['txid']
        sleep(0.265)
        query = self.messenger.post('/private/QueryOrders', {'txid': txid})
        if self.has_error(query):
            return query['error']
        info = query['result'][txid]
        return {
            'id': info['descr']['pair'],
            'side': info['descr']['type'],
            'price': info['price'],
            'size': info['vol'],
            'timestamp': epoch_to_datetime(info['opentm'])
        }


class KrakenFactory(AbstractFactory):
    def get_client(self, key: str, secret: str) -> AbstractClient:
        auth = Auth(key, secret)
        messenger = Messenger(auth)
        return KrakenClient(messenger)
