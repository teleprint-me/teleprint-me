import abc


class AbstractClient(abc.ABC):
    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def client(self) -> object:
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
    def get_price(self, asset: str) -> dict:
        pass

    @abc.abstractmethod
    def post_order(self, json: dict) -> dict:
        pass


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def get_client(self) -> AbstractClient:
        pass
