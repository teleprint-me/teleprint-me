from os import environ, path
from uuid import uuid4

from coinbase_pro import client
from peewee import (
    BooleanField,
    DoesNotExist,
    ForeignKeyField,
    Model,
    ModelSelect,
    SqliteDatabase,
    TextField,
)
from playhouse.shortcuts import model_to_dict

#
# Environment
#
instance_path = environ.get("INSTANCE_PATH", f'{environ.get("PWD")}/instance')
database_name = environ.get("DATABASE_NAME", "database.sqlite")
database_path = path.join(instance_path, database_name)
settings_name = environ.get("SETTINGS_NAME", "settings.json")
settings_path = path.join(instance_path, settings_name)

#
# Peewee Database
#
pragmas = {
    "journal_mode": "wal",
    "wal_autocheckpoint": True,
    "foreign_keys": True,
    "permanent": True,
}

database = SqliteDatabase(database_path, pragmas=pragmas)


#
# Peewee Models
#
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
    quote = TextField()
    quote_fee = TextField(default=f"{0.:.8f}")
    quote_total = TextField()
    quote_prev = TextField(default=f"{0.:.8f}")
    base = TextField()
    base_fee = TextField(default=f"{0.:.8f}")
    base_total = TextField()
    base_prev = TextField(default=f"{0.:.8f}")
    period = TextField(default="0")
    strategy = ForeignKeyField(Strategy, backref="datum")


#
# Set Schema
#
def initialize():
    database.connect()
    database.create_tables([User, Interface, Strategy, Data])
    database.close()


#
# Model
#
def get_model(cls: Model, attr: str, val: object) -> object:
    try:
        return cls.get(getattr(cls, attr) == val)
    except (DoesNotExist,):
        return None


#
# User
#
def get_user(name: str) -> User:
    return get_model(User, "name", name)


def user_to_dict(user: User) -> dict:
    return model_to_dict(user, exclude=[User.password, User.key, User.sid])


#
# Interface
#
def get_interface(name: str) -> Interface:
    return get_model(Interface, "name", name)


def get_interface_list(user: User) -> list[dict]:
    return [interface_to_dict(i) for i in user.interfaces]


def get_interface_active(interfaces: ModelSelect) -> Interface:
    try:
        return [i for i in interfaces if i.active][0]
    except (IndexError,):
        return None


def set_interface_active(user: User, interface: Interface) -> int:
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
        return Interface.bulk_update(selection, fields=["active"], batch_size=10)


def interface_to_dict(interface: Interface) -> dict:
    return model_to_dict(
        interface, exclude=[Interface.secret, Interface.passphrase, Interface.user]
    )


#
# Strategy
#
def get_strategy(name: str) -> Strategy:
    return get_model(Strategy, "name", name)


def get_strategy_list(user: User) -> list[dict]:
    return [strategy_to_dict(s) for s in user.strategies]


def strategy_to_dict(strategy: Strategy) -> dict:
    try:
        return model_to_dict(strategy, exclude=[Strategy.user])
    except (AttributeError,):
        return None


#
# Data
#
def get_data(strategy: Strategy) -> Data:
    return get_model(Data, "period", strategy.period)


def get_data_list(strategy: Strategy) -> dict:
    return [model_to_dict(d, exclude=[Data.strategy]) for d in strategy.datum]


def data_to_dict(strategy: Strategy) -> dict:
    return model_to_dict(get_data(strategy), exclude=[Data.strategy])


def get_data_basis(strategy: Strategy) -> dict:
    bought, sold = 0, 0
    for data in strategy.datum:
        if data.side == "buy":
            bought += float(data.quote)
        if data.side == "sell":
            sold += float(data.quote)
    return {"bought": bought, "sold": sold, "cost": bought - sold}


#
# Client
#
def get_client(interface: Interface) -> client.CoinbasePro:
    try:
        return client.get_client(
            model_to_dict(
                interface,
                exclude=[
                    Interface.id,
                    Interface.name,
                    Interface.active,
                    Interface.user,
                ],
            )
        )
    except (AttributeError,):
        return None
