from os import environ, path
from uuid import uuid4

from peewee import (
    BooleanField,
    DoesNotExist,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    TextField,
)
from playhouse.shortcuts import model_to_dict

instance_path = environ.get("INSTANCE_PATH", f'{environ.get("PWD")}/instance')
database_name = environ.get("DATABASE_NAME", "database.sqlite")
database_path = path.join(instance_path, database_name)
settings_name = environ.get("SETTINGS_NAME", "settings.json")
settings_path = path.join(instance_path, settings_name)

pragmas = {
    "journal_mode": "wal",
    "wal_autocheckpoint": True,
    "foreign_keys": True,
    "permanent": True,
}

database = SqliteDatabase(database_path, pragmas=pragmas)


class Base(Model):
    class Meta:
        database = database


class User(Base):
    name = TextField(unique=True)  # username/email
    password = TextField()  # hashed password
    key = TextField(default=str())  # encryption key
    currency = TextField(default="USD")  # quote currency
    theme = TextField(default="Light")  # applied ui theme
    sid = TextField(unique=True, default=str(uuid4()))


class Interface(Base):
    name = TextField(unique=True)  # label
    key = TextField(unique=True)  # key
    secret = TextField()  # secret
    passphrase = TextField()  # passphrase
    rest = TextField(default="https://api.pro.coinbase.com")  # api url
    feed = TextField(default="wss://ws-feed.pro.coinbase.com")  # wss url
    active = BooleanField(default=False)  # in use?
    user = ForeignKeyField(User, backref="interfaces")


class Strategy(Base):
    name = TextField(unique=True)  # strategy identifier
    base = TextField()  # product base: BTC
    quote = TextField()  # product quote: USD
    product = TextField()  # product: BTC-USD
    type_ = TextField()  # strategy type: cost or value average
    frequency = TextField()  # daily, weekly, monthly, yearly
    principal = TextField()  # principal amount
    yield_ = TextField(default="0")  # annual percentage yield
    period = TextField(default="0")  # targets current period
    user = ForeignKeyField(User, backref="strategies")


class Data(Base):
    date = TextField()
    price = TextField()
    target = TextField()
    value = TextField()
    recommend = TextField()
    side = TextField()
    base = TextField()
    base_fee = TextField(default=f"{0.:.8f}")
    base_total = TextField()
    base_prev = TextField(default=f"{0.:.8f}")
    quote = TextField()
    quote_fee = TextField(default=f"{0.:.8f}")
    quote_total = TextField()
    quote_prev = TextField(default=f"{0.:.8f}")
    period = TextField(default="0")
    strategy = ForeignKeyField(Strategy, backref="datum")


def initialize():
    database.connect()
    database.create_tables([User, Interface, Strategy, Data])
    database.close()


def get_model(cls: Model, attr: str, val: object) -> object:
    try:
        return cls.get(getattr(cls, attr) == val)
    except (DoesNotExist,):
        return None


def get_user(name: str) -> User:
    return get_model(User, "name", name)


def get_interface(name: str) -> Interface:
    return get_model(Interface, "name", name)


def get_strategy(name: str) -> Strategy:
    return get_model(Strategy, "name", name)


def get_data(strategy: Strategy) -> Data:
    return get_model(Data, "period", strategy.period)


def user_to_dict(user: User) -> dict:
    return model_to_dict(user, exclude=[User.password, User.key, User.sid])


def interface_to_dict(interface: Interface) -> dict:
    return model_to_dict(
        interface, exclude=[Interface.secret, Interface.passphrase, Interface.user]
    )


def get_interface_list(user: User) -> list[dict]:
    return [interface_to_dict(i) for i in user.interfaces]


def strategy_to_dict(strategy: Strategy) -> dict:
    return model_to_dict(strategy, exclude=[Strategy.user])


def get_strategy_list(user: User) -> list[dict]:
    return [strategy_to_dict(s) for s in user.strategies]


def data_to_dict(strategy: Strategy) -> dict:
    return model_to_dict(get_data(strategy), exclude=[Data.strategy])


def get_data_list(strategy: Strategy) -> dict:
    return [model_to_dict(d, exclude=[Data.strategy]) for d in strategy.datum]
