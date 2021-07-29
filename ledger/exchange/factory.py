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
import abc
import requests

__agent__ = 'teleprint.me'
__source__ = 'https://github.com/teleprint-me/ledger'
__version__ = '0.0.x'


class AbstractToken(abc.ABC):
    @abc.abstractproperty
    def key(self) -> str:
        pass

    @abc.abstractproperty
    def secret(self) -> str:
        pass

    @abc.abstractproperty
    def passphrase(self) -> str:
        pass

    @abc.abstractmethod
    def as_dict(self) -> dict:
        pass


class AbstractAuth(abc.ABC):
    @abc.abstractproperty
    def token(self) -> AbstractToken:
        pass


class AbstractAPI(abc.ABC):
    @abc.abstractproperty
    def version(self) -> int:
        """return the current rest api version"""
        pass

    @abc.abstractproperty
    def options(self) -> dict:
        """get the dictionary for response.json"""
        pass

    @abc.abstractproperty
    def url(self) -> str:
        """return the kraken rest api url"""
        pass

    @abc.abstractmethod
    def endpoint(self, value: str) -> str:
        """return a endpoint based on `value`"""
        pass

    @abc.abstractmethod
    def path(self, value: str) -> str:
        """return the full path based on url and endpoint `value`"""
        pass


class AbstractMessenger(abc.ABC):
    @abc.abstractproperty
    def auth(self) -> AbstractAuth:
        pass

    @abc.abstractproperty
    def api(self) -> AbstractAPI:
        pass

    @abc.abstractproperty
    def timeout(self) -> int:
        pass

    @abc.abstractproperty
    def options(self) -> dict:
        pass

    @abc.abstractproperty
    def session(self) -> requests.Session:
        pass

    @abc.abstractproperty
    def response(self) -> requests.Response:
        pass

    @abc.abstractmethod
    def get(self, endpoint: str, params: dict) -> object:
        pass

    @abc.abstractmethod
    def post(self, endpoint: str, data: dict) -> object:
        pass

    @abc.abstractmethod
    def page(self, endpoint: str, params: dict) -> object:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass


class AbstractContext(abc.ABC):
    def __init__(self, endpoint: str, params: dict):
        pass

    @abc.abstractproperty
    def endpoint(self) -> str:
        pass

    @abc.abstractproperty
    def params(self) -> dict:
        pass

    @abc.abstractproperty
    def asset(self) -> str:
        pass

    @abc.abstractproperty
    def callback(self) -> object:
        pass


class AbstractClient(abc.ABC):
    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def messenger(self) -> AbstractMessenger:
        pass

    @abc.abstractmethod
    def get_assets(self) -> list:
        pass

    @abc.abstractmethod
    def get_accounts(self) -> list:
        pass

    @abc.abstractmethod
    def get_history(self, asset: str) -> list:
        pass

    @abc.abstractmethod
    def get_deposits(self, asset: str) -> list:
        pass

    @abc.abstractmethod
    def get_withdrawals(self, asset: str) -> list:
        pass

    @abc.abstractmethod
    def get_price(self, asset: str) -> dict:
        pass

    @abc.abstractmethod
    def post_order(self, json: dict) -> dict:
        pass


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def get_client(self) -> AbstractClient:
        pass
