from dataclasses import dataclass, field

from coinbase_pro import client
from peewee import DoesNotExist, Model
from playhouse.shortcuts import model_to_dict
from teleprint_me.core.sqlite import Data, Interface, Strategy, User, database

batch_size = 25

# this is super messy and needs to get cleaned up.
exclude_user = [User.password, User.key, User.sid]
exclude_interface = [Interface.secret, Interface.passphrase, Interface.user]
exclude_interface_settings = [Interface.name, Interface.active, Interface.user]
exclude_interface_client = [
    Interface.id,
    Interface.name,
    Interface.active,
    Interface.user,
]
exclude_strategy = [Strategy.user]
exclude_data = [Data.strategy]
exclude = [
    exclude_user,
    exclude_interface,
    exclude_interface_settings,
    exclude_interface_client,
    exclude_strategy,
    exclude_data,
]

fields_user = ["name", "currency", "theme"]
fields_interface = ["name", "key", "rest", "feed", "active"]
fields_strategy = [
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
fields_data = [
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
fields = [fields_user, fields_interface, fields_strategy, fields_data]


@dataclass
class ProxyExclude:
    user: list = field(default_factory=list)
    interface: list = field(default_factory=list)
    settings: list = field(default_factory=list)
    client: list = field(default_factory=list)
    strategy: list = field(default_factory=list)
    data: list = field(default_factory=list)


@dataclass
class ProxyField:
    user: list[str] = field(default_factory=list)
    interface: list[str] = field(default_factory=list)
    strategy: list[str] = field(default_factory=list)
    data: list[str] = field(default_factory=list)


class ProxyBuild:
    @classmethod
    def model(cls: Model, attr: str, val: object) -> object:
        try:
            return cls.get(getattr(cls, attr) == val)
        except (DoesNotExist,):
            return None

    def user(self, name: str) -> User:
        return self.model(User, "name", name)

    def interface(self, name: str) -> Interface:
        return self.model(Interface, "name", name)

    def strategy(self, name: str) -> Strategy:
        return self.model(Strategy, "name", name)

    def data(self, period: str) -> Data:
        return self.model(Data, "period", period)


class ProxyModel:
    def __init__(self):
        self.__field = ProxyField(*fields)
        self.__exclude = ProxyExclude(*exclude)
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


class ProxyUser(ProxyModel):
    def to_dict(self, user: User) -> dict:
        return self.model.to_dict(user, exclude=self.exclude.user)


class ProxyInterface(ProxyModel):
    def to_dict(self, name: str) -> dict:
        return self.model.to_dict(
            self.model.build.interface(name), exclude=self.exclude.interface
        )

    def to_settings(self, name: str) -> dict:
        return self.model.to_dict(
            self.model.build.interface(name), exclude=self.exclude.settings
        )

    def to_list(self, user: User) -> list[dict]:
        return [self.to_dict(i) for i in user.interfaces]

    # get_active and set_active, while related, may be better off in a
    # seperate class. there are no pre-existing classes or methods
    # that do something similar. plan something out to apply SoC.
    @staticmethod
    def get_active(user: User) -> Interface:
        try:
            return [i for i in user.interfaces if i.active][0]
        except (IndexError,):
            return None

    @staticmethod
    def set_active(user: User, interface: Interface) -> int:
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
        with database.atomic():
            return Interface.bulk_update(
                selection, fields=["active"], batch_size=batch_size
            )

    def get_client(self, interface: Interface) -> client.CoinbasePro:
        try:
            return client.get_client(
                model_to_dict(
                    interface,
                    exclude=self.exclude.client,
                )
            )
        except (AttributeError,):
            return None


class ProxyStrategy(ProxyModel):
    def to_dict(self, name: str) -> dict:
        return self.model.to_dict(
            self.model.build.strategy(name), exclude=self.exclude.strategy
        )

    def to_list(self, user: User) -> list[dict]:
        return [
            self.model.to_dict(s, exclude=self.exclude.strategy)
            for s in user.strategies
        ]

    # get_yield and get_target methods may be better off in a
    # seperate class... core/product already does something similar.
    # maybe figure something out with that instead.
    @staticmethod
    def get_yield(strategy: Strategy) -> dict:
        frequency = {"monthly": 12, "weekly": 52, "daily": 365}.get(
            strategy.frequency, 12
        )
        yield_ = 1 + (float(strategy.yield_) / frequency)
        return {"yield_": yield_, "frequency": frequency}

    def get_target(self, strategy: Strategy) -> dict:
        principal = float(strategy.principal)
        period = int(strategy.period)
        yield_ = self.get_yield(strategy)
        if strategy.type_ == "value_average":
            return {"value": principal * period * (yield_["value"] ** period)}
        return {"value": principal * period}


class ProxyData(ProxyModel):
    def to_dict(self, strategy: Strategy) -> dict:
        return self.model.to_dict(strategy.datum, exclude=self.exclude.data)

    def to_list(self, strategy: Strategy) -> list[dict]:
        return [
            self.model.to_dict(d, exclude=self.exclude.data) for d in strategy.datum
        ]

    @staticmethod
    def get_basis(strategy: Strategy) -> dict:
        bought, sold = 0, 0
        for data in strategy.datum:
            if data.side == "buy":
                bought += float(data.quote)
            if data.side == "sell":
                sold += float(data.quote)
        return {"bought": bought, "sold": sold, "cost": bought - sold}

    @staticmethod
    def get_average(strategy: Strategy) -> dict:
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


@dataclass
class ProxyDatabase:
    user: ProxyUser = None
    interface: ProxyInterface = None
    strategy: ProxyStrategy = None
    data: ProxyData = None


def get_proxy_database() -> ProxyDatabase:
    return ProxyDatabase(ProxyUser(), ProxyInterface(), ProxyStrategy(), ProxyData())
