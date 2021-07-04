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

from ledger.exchange.kraken.auth import Auth
from ledger.exchange.kraken.messenger import Messenger

import datetime
import time


def epoch2datetime(timestamp: float) -> str:
    '''convert timestamp from epoch to iso 8601'''
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.isoformat()


def pricelist2average(prices: list) -> str:
    '''return average price based on approx bids and asks at market value'''
    pricelist = sum(float(p) for p in prices) / len(prices)
    return f'{pricelist:.5f}'


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

    def has_error(self, response: object) -> bool:
        return bool(response.get('error'))

    def get_assets(self) -> list:
        assets = list()
        response = self.messenger.get('/public/AssetPairs')
        if self.has_error(response):
            return response['error']
        result = response['result']
        for k, v in result.items():
            assets.append({
                'id': k,
                'display': v.get('wsname'),
                'name': v.get('base'),
                'min-size': v.get('ordermin')
            })
        return assets

    def get_accounts(self) -> list:
        accounts = list()
        response = self.messenger.post('/private/Balance')
        if self.has_error(response):
            return response['error']
        result = response['result']
        for k, v in result.items():
            accounts.append({
                'name': k,
                'balance': v
            })
        return accounts

    def get_history(self, asset: str, limit: int = None) -> list:
        limit = 250 if limit is None else limit
        offset = 0
        fills = list()
        while offset < limit:
            response = self.messenger.post(
                '/private/TradesHistory', {'ofs': offset}
            )
            if self.has_error(response):
                return response['error']
            trades = response['result']['trades']
            for fill in trades.values():
                if fill['pair'] == asset:
                    fills.append({
                        'timestamp': epoch2datetime(fill['time']),
                        'id': fill['pair'],
                        'side': fill['type'],
                        'price': fill['price'],
                        'size': fill['vol']
                    })
            offset += 50
            time.sleep(0.25)
        return fills

    def get_price(self, asset: str) -> dict:
        response = self.messenger.get('/public/Ticker', {'pair': asset})
        if self.has_error(response):
            return response['error']
        asset = response['result'][asset]
        return {
            'bid': asset['b'][0],
            'ask': asset['a'][0],
            'price': pricelist2average(asset['p'])
        }

    def post_order(self, data: dict) -> dict:
        order = self.messenger.post('/private/AddOrder', data)
        if self.has_error(order):
            return order['error']
        txid = order['result']['txid']
        time.sleep(0.25)
        query = self.messenger.post('/private/QueryOrders', {'txid': txid})
        if self.has_error(query):
            return query['error']
        info = query['result'][txid]
        return {
            'timestamp': epoch2datetime(info['opentm']),
            'id': info['descr']['pair'],
            'side': info['descr']['type'],
            'price': info['price'],
            'size': info['vol']
        }


class KrakenFactory(AbstractFactory):
    def get_client(self, key: str, secret: str) -> AbstractClient:
        auth = Auth(key, secret)
        messenger = Messenger(auth)
        return KrakenClient(messenger)
