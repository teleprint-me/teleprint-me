from os import environ, path
from uuid import uuid4

from peewee import (
    BooleanField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

#
# Environment
#
instance_path = environ.get("INSTANCE_PATH", f'{environ.get("PWD")}/instance')
database_name = environ.get("DATABASE_NAME", "teleprint-me.sqlite")
database_path = path.join(instance_path, database_name)
settings_name = environ.get("SETTINGS_NAME", "settings.json")
settings_path = path.join(instance_path, settings_name)


#
# Database
#
pragmas = {
    "journal_mode": "wal",
    "wal_autocheckpoint": True,
    "foreign_keys": True,
    "permanent": True,
}

database = SqliteDatabase(database_path, pragmas=pragmas)


#
# Models
#
class Base(Model):
    class Meta:
        database = database


class User(Base):
    name = TextField(unique=True)  # username/email
    password = TextField()  # hashed password
    key = TextField(default=str())  # encryption key
    currency = TextField(default="USD")  # quote currency
    theme = TextField(default="light")  # applied ui theme
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
    principal = FloatField()  # principal amount
    yield_ = FloatField(default=float())  # annual percentage yield
    period = IntegerField(default=int())  # targets current period
    user = ForeignKeyField(User, backref="strategies")


class Data(Base):
    date = DateTimeField()
    price = FloatField()
    target = FloatField()
    value = FloatField()
    recommend = FloatField()
    side = TextField()
    quote = FloatField()
    quote_fee = FloatField(default=float())
    quote_total = FloatField()
    quote_prev = FloatField(default=float())
    base = FloatField()
    base_fee = FloatField(default=float())
    base_total = FloatField()
    base_prev = FloatField(default=float())
    period = IntegerField(default=int())
    strategy = ForeignKeyField(Strategy, backref="datum")


#
# Set Schema
#
def initialize():
    database.connect()
    database.create_tables([User, Interface, Strategy, Data])
    database.close()
