from coinbase_pro.client import CoinbasePro
from teleprint_me.proxy.client import ProxyClient
from teleprint_me.proxy.database import (
    ProxyData,
    ProxyDatabase,
    ProxyInterface,
    ProxyStrategy,
    ProxyUser,
)


class Proxy:
    def __init__(self, client: CoinbasePro = None):
        self.__client = ProxyClient(client) if client else None
        self.__database = ProxyDatabase(
            ProxyUser(), ProxyInterface(), ProxyStrategy(), ProxyData()
        )

    @property
    def client(self) -> ProxyClient:
        return self.__client

    @client.setter
    def client(self, client: CoinbasePro):
        self.__client = client

    @property
    def database(self) -> ProxyDatabase:
        return self.__database
