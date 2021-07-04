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
from ledger.exchange.factory import AbstractAPI
from ledger.exchange.factory import AbstractMessenger

from ledger.exchange.kraken.auth import Auth

import requests


class API(AbstractAPI):
    def __init__(self):
        self.__options = {}

    @property
    def version(self) -> int:
        return 0

    @property
    def options(self) -> dict:
        return self.__options

    @options.setter
    def options(self, value: dict) -> None:
        """set the dictionary for response.json"""
        assert isinstance(value, dict), '`value` must be of type dict'
        self.__options = value

    @property
    def url(self) -> str:
        return 'https://api.kraken.com'

    def endpoint(self, value: str) -> str:
        return f'/{self.version}/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Messenger(AbstractMessenger):
    def __init__(self, auth: Auth = None) -> None:

        self.__auth = auth
        self.__api = API()
        self.__timeout = 30
        self.__session = requests.Session()
        self.__response = None

    @property
    def auth(self) -> Auth:
        return self.__auth

    @property
    def api(self) -> API:
        return self.__api

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def options(self) -> dict:
        return self.__api.options

    @options.setter
    def options(self, value: dict) -> None:
        self.__api.options = value

    @property
    def session(self) -> requests.Session:
        return self.__session

    @property
    def response(self) -> requests.Response:
        return self.__response

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = self.api.path(endpoint)
        endpoint = self.api.endpoint(endpoint)

        if not params:
            params = dict()

        params['nonce'] = self.auth.nonce
        headers = self.auth(endpoint, params)

        self.__response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        return self.__response.json(**self.options)

    def post(self, endpoint: str, data: dict = None) -> dict:
        url = self.api.path(endpoint)
        endpoint = self.api.endpoint(endpoint)

        if not data:
            data = dict()

        data['nonce'] = self.auth.nonce
        headers = self.auth(endpoint, data)

        self.__response = self.session.post(
            url,
            data=data,
            headers=headers,
            timeout=self.timeout
        )

        return self.__response.json(**self.options)

    def page(self, endpoint: str, params: dict = None) -> dict:
        pass

    def close(self) -> None:
        self.session.close()
