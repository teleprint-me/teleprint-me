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
from ledger.exchange.factory import __agent__
from ledger.exchange.factory import __source__
from ledger.exchange.factory import __version__

from ledger.exchange.factory import AbstractToken
from ledger.exchange.factory import AbstractAuth

import base64
import hashlib
import hmac
import urllib
import time


class Token(AbstractToken):
    def __init__(self, key: str, secret: str, passphrase: str = None):
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase

    @property
    def key(self) -> str:
        return self.__key

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def passphrase(self) -> str:
        return self.__passphrase

    def as_dict(self) -> dict:
        return {
            'key': self.key,
            'secret': self.secret
        }


def get_timestamp() -> str:
    return str(int(1000 * time.time()))


def get_message(endpoint: str, data: dict) -> bytes:
    post = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + post).encode()
    return endpoint.encode() + hashlib.sha256(encoded).digest()


def get_signature(endpoint: str, data: dict, secret: str) -> bytes:
    message = get_message(endpoint, data)
    secret = base64.b64decode(secret)
    signature = hmac.new(secret, message, hashlib.sha512)
    b64signature = base64.b64encode(signature.digest())
    return b64signature.decode()


def get_headers(signature: bytes, key: str) -> dict:
    return {
        'User-Agent': f'{__agent__}/{__version__} {__source__}',
        'API-Key': key,
        'API-Sign': signature,
    }


class Auth(AbstractAuth):
    def __init__(self, key: str, secret: str):
        self.__token = Token(key, secret)

    def __call__(self, endpoint: str, data: dict) -> dict:
        signature = get_signature(endpoint, data, self.__token.secret)
        return get_headers(signature, self.__token.key)

    @property
    def token(self) -> Token:
        return self.__token

    @property
    def nonce(self) -> str:
        return get_timestamp()
