from os import environ
from os import path

from peewee import Model
from peewee import BooleanField
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import SqliteDatabase

from uuid import uuid4

instance_path = environ.get('INSTANCE_PATH', f'{environ.get("PWD")}/instance')
database_name = environ.get('DATABASE_NAME', 'database.sqlite')
database_path = path.join(instance_path, database_name)
settings_name = environ.get('SETTINGS_NAME', 'settings.json')
settings_path = path.join(instance_path, settings_name)

pragmas = {
    'journal_mode': 'wal',
    'wal_autocheckpoint': True,
    'foreign_keys': True,
    'permanent': True
}

database = SqliteDatabase(database_path, pragmas=pragmas)


class Base(Model):
    class Meta:
        database = database


class User(Base):
    name = TextField(unique=True)         # username/email
    password = TextField()                # hashed password
    key = TextField(default=str())        # encryption key
    currency = TextField(default='USD')   # quote currency
    theme = TextField(default='Light')    # applied ui theme
    sid = TextField(unique=True, default=str(uuid4()))


class Interface(Base):
    name = TextField(unique=True)                               # label
    key = TextField(unique=True)                                # key
    secret = TextField()                                        # secret
    passphrase = TextField()                                    # passphrase
    rest = TextField(default='https://api.pro.coinbase.com')    # api url
    feed = TextField(default='wss://ws-feed.pro.coinbase.com')  # wss url
    active = BooleanField(default=False)                        # in use?
    user = ForeignKeyField(User, backref='interfaces')


class Strategy(Base):
    name = TextField(unique=True)      # strategy identifier
    base = TextField()                 # product base: BTC
    quote = TextField()                # product quote: USD
    product = TextField()              # product: BTC-USD
    type_ = TextField()                # strategy type: cost or value average
    frequency = TextField()            # daily, weekly, monthly, yearly
    principal = TextField()            # principal amount
    yield_ = TextField(default='0')    # annual percentage yield
    period = TextField(default='1')    # targets current period
    user = ForeignKeyField(User, backref='strategies')


class Dataset(Base):
    date = DateTimeField()
    price = TextField()
    target = TextField()
    value = TextField()
    recommend = TextField()
    side = TextField()
    base = TextField()
    base_fee = TextField(default=f'{0.:.8f}')
    base_total = TextField()
    base_prev = TextField(default=f'{0.:.8f}')
    quote = TextField()
    quote_fee = TextField(default=f'{0.:.8f}')
    quote_total = TextField()
    quote_prev = TextField(default=f'{0.:.8f}')
    period = TextField(default='1')
    strategy = ForeignKeyField(Strategy, backref='datasets')


def initialize():
    database.connect()
    database.create_tables([User, Interface, Strategy, Dataset])
    database.close()
