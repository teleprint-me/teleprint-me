from os import environ
from os import path

from peewee import Model
from peewee import BooleanField
from peewee import IntegerField
from peewee import FloatField
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import SqliteDatabase

from uuid import uuid4

instance_path = environ.get('INSTANCE_PATH', f'{environ.get("PWD")}/instance')
database_name = environ.get('DATABASE_NAME', 'database.sqlite')
database_path = path.join(instance_path, database_name)

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
    name = TextField(unique=True)        # username/email
    password = TextField()               # hashed password
    sid = TextField(unique=True, default=str(uuid4()))


class Setting(Base):
    currency = TextField(default='USD')  # quote currency
    theme = TextField(default='Light')   # applied ui theme
    user = ForeignKeyField(User, backref='settings')


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
    # unique table identifier: str(uuid4())
    table_id = TextField(unique=True, default=str(uuid4()))
    name = TextField()            # label
    product_id = TextField()             # product identifier: BTC-USD
    frequency = TextField()       # daily, weekly, monthly, yearly
    principal = FloatField()      # principal amount
    apy = FloatField()            # annual percentage yield
    period = IntegerField()       # targets current period
    user = ForeignKeyField(User, backref='strategies')


class Data(Base):
    date = DateTimeField()
    price = FloatField()
    target = FloatField()
    value = FloatField()
    recommend = FloatField()
    side = TextField()
    base = FloatField()
    base_fee = FloatField(default=0.)
    base_total = FloatField()
    base_prev = FloatField(default=0.)
    quote = FloatField()
    quote_fee = FloatField(default=0.)
    quote_total = FloatField()
    quote_prev = FloatField(default=0.)
    period = IntegerField()


def init_database(db: SqliteDatabase):
    db.connect()
    db.create_tables([User, Setting, Interface, Strategy])
    db.close()
