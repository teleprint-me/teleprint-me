from dataclasses import dataclass

from coinbase_pro import client
from peewee import DoesNotExist, Model
from playhouse.shortcuts import model_to_dict
from teleprint_me.core import sqlite

batch_size = 25


class ProxyExclude:
    def __init__(self):
        self.__user = [sqlite.User.password, sqlite.User.key, sqlite.User.sid]
        self.__interface = [
            sqlite.Interface.secret,
            sqlite.Interface.passphrase,
            sqlite.Interface.user,
        ]
        self.__settings = [
            sqlite.Interface.name,
            sqlite.Interface.active,
            sqlite.Interface.user,
        ]
        self.__client = [
            sqlite.Interface.id,
            sqlite.Interface.name,
            sqlite.Interface.active,
            sqlite.Interface.user,
        ]
        self.__strategy = [sqlite.Strategy.user]
        self.__data = [sqlite.Data.strategy]

    @property
    def user(self) -> list[object]:
        return self.__user

    @property
    def interface(self) -> list[object]:
        return self.__interface

    @property
    def settings(self) -> list[object]:
        return self.__settings

    @property
    def client(self) -> list[object]:
        return self.__client

    @property
    def strategy(self) -> list[object]:
        return self.__strategy

    @property
    def data(self) -> list[object]:
        return self.__data


class ProxyField:
    def __init__(self):
        self.__user = ["name", "currency", "theme"]
        self.__interface = ["name", "key", "rest", "feed", "active"]
        self.__strategy = [
            "name",
            "base",
            "quote",
            "product",
            "type_",
            "frequency",
            "principal",
            "yield_",
            "period",
        ]
        self.__data = [
            "date",
            "price",
            "target",
            "value",
            "recommend",
            "side",
            "quote",
            "quote_fee",
            "quote_total",
            "quote_prev",
            "base",
            "base_fee",
            "base_total",
            "base_prev",
            "period",
        ]

    @property
    def user(self) -> list[str]:
        return self.__user

    @property
    def interface(self) -> list[str]:
        return self.__interface

    @property
    def strategy(self) -> list[str]:
        return self.__strategy

    @property
    def data(self) -> list[str]:
        return self.__data


class ProxyBuild:
    @classmethod
    def model(self, cls: Model, attr: str, val: object) -> object:
        try:
            return cls.get(getattr(cls, attr) == val)
        except (DoesNotExist,):
            return None

    def user(self, name: str) -> sqlite.User:
        return self.model(sqlite.User, "name", name)

    def interface(self, name: str) -> sqlite.Interface:
        return self.model(sqlite.Interface, "name", name)

    def strategy(self, name: str) -> sqlite.Strategy:
        return self.model(sqlite.Strategy, "name", name)

    def data(self, strategy: sqlite.Strategy) -> sqlite.Data:
        pass


class ProxyModel:
    def __init__(self):
        self.__field = ProxyField()
        self.__exclude = ProxyExclude()
        self.__build = ProxyBuild()

    @property
    def field(self) -> ProxyField:
        return self.__field

    @property
    def exclude(self) -> ProxyExclude:
        return self.__exclude

    @property
    def build(self) -> ProxyBuild:
        return self.__build

    def to_dict(self, model: Model, exclude: list = None) -> dict:
        try:
            return model_to_dict(model, exclude=exclude)
        except (AttributeError,):
            return None


class ProxyBase:
    def __init__(self):
        self.__model = ProxyModel()

    @property
    def model(self) -> ProxyModel:
        return self.__model


class ProxyUser(ProxyBase):
    def to_dict(self, user: sqlite.User) -> dict:
        return self.model.to_dict(user, exclude=self.model.exclude.user)

    def get(self, name: str) -> sqlite.User:
        return self.model.build.user(name)


class ProxyInterface(ProxyBase):
    def to_dict(self, interface: sqlite.Interface) -> dict:
        return self.model.to_dict(interface, exclude=self.model.exclude.interface)

    def to_settings(self, interface: sqlite.Interface) -> dict:
        return self.model.to_dict(interface, exclude=self.model.exclude.settings)

    def to_list(self, user: sqlite.User) -> list[dict]:
        return [
            self.model.to_dict(interface, exclude=self.model.exclude.interface)
            for interface in user.interfaces
        ]

    def get(self, name: str) -> sqlite.Interface:
        return self.model.build.interface(name)

    def get_client(self, interface: sqlite.Interface) -> client.CoinbasePro:
        try:
            return client.get_client(
                self.model.to_dict(
                    interface,
                    exclude=self.model.exclude.client,
                )
            )
        except (AttributeError,) as e:
            print("[ProxyInterface]", self, "[interface]", interface.name, "[error]", e)
            return None

    @staticmethod
    def get_active(user: sqlite.User) -> sqlite.Interface:
        try:
            return [interface for interface in user.interfaces if interface.active][0]
        except (IndexError,):
            return None

    @staticmethod
    def set_active(user: sqlite.User, interface: sqlite.Interface) -> int:
        selection = []
        if 1 == len(user.interfaces):
            interface.active = True
            return interface.save()
        for i in user.interfaces:
            if i == interface:
                i.active = True
            else:
                i.active = False
            selection.append(i)
        with sqlite.database.atomic():
            return sqlite.Interface.bulk_update(
                selection, fields=["active"], batch_size=batch_size
            )


class ProxyStrategy(ProxyBase):
    def to_dict(self, strategy: sqlite.Strategy) -> dict:
        return self.model.to_dict(strategy, exclude=self.exclude.strategy)

    def to_list(self, user: sqlite.User) -> list[dict]:
        return [
            self.model.to_dict(strategy, exclude=self.exclude.strategy)
            for strategy in user.strategies
        ]

    def get(self, name: str) -> Model:
        return self.model.build.strategy(name)

    def get_frequency(self, strategy) -> int:
        return {"monthly": 12, "weekly": 52, "daily": 365}.get(strategy.frequency, 12)

    def get_yield(self, strategy: sqlite.Strategy) -> float:
        return 1 + (strategy.yield_ / self.to_frequency(strategy))

    def get_target(self, strategy: sqlite.Strategy) -> float:
        if strategy.period == 1:
            return strategy.principal
        if strategy.type_ == "value_average":
            return (
                strategy.principal
                * strategy.period
                * (self.get_yield(strategy) ** strategy.period)
            )
        return strategy.principal * strategy.period


class ProxyData(ProxyBase):
    def to_dict(self, strategy: sqlite.Strategy) -> dict:
        return self.model.to_dict(strategy.datum, exclude=self.exclude.data)

    def to_list(self, strategy: sqlite.Strategy) -> list[dict]:
        return [
            self.model.to_dict(d, exclude=self.exclude.data) for d in strategy.datum
        ]

    @staticmethod
    def get_basis(strategy: sqlite.Strategy) -> dict:
        bought, sold = 0, 0
        for data in strategy.datum:
            if data.side == "buy":
                bought += float(data.quote)
            if data.side == "sell":
                sold += float(data.quote)
        return {"bought": bought, "sold": sold, "cost": bought - sold}

    @staticmethod
    def get_average(strategy: sqlite.Strategy) -> dict:
        n, average = float(), float()
        for data in strategy.datum:
            if data.side == "buy":
                n += 1
                average += float(data.price)
        if n > 0:
            average /= n
        else:
            average = 0.0
        return {"price": average, "size": n}


@dataclass(frozen=True)
class ProxyDatabase:
    user: ProxyUser
    interface: ProxyInterface
    strategy: ProxyStrategy
    data: ProxyData
