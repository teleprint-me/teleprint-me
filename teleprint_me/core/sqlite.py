from os import environ
from os import remove
from os import scandir
from os.path import join

from sqlite3 import connect
from sqlite3 import Connection
from sqlite3 import Row

from typing import Any
from typing import Iterable


class QuerySchema(object):
    @staticmethod
    def user() -> str:
        return 'CREATE TABLE user (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'name TEXT NOT NULL UNIQUE, ' \
            'password TEXT NOT NULL, ' \
            'interface TEXT NOT NULL, ' \
            'websocket TEXT NOT NULL, ' \
            'currency TEXT NOT NULL, ' \
            'theme TEXT NOT NULL)'

    @staticmethod
    def interface(self) -> str:
        return 'CREATE TABLE interface (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'name TEXT NOT NULL UNIQUE, ' \
            'key TEXT NOT NULL, ' \
            'secret TEXT NOT NULL, ' \
            'passphrase TEXT NOT NULL)'

    @staticmethod
    def strategy() -> str:
        return 'CREATE TABLE strategy (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'table_id TEXT NOT NULL UNIQUE, ' \
            'name TEXT NOT NULL, ' \
            'product_id TEXT NOT NULL, ' \
            'frequency TEXT NOT NULL, ' \
            'principal REAL NOT NULL, ' \
            'apy REAL NOT NULL, ' \
            'period INTEGER NOT NULL)'

    @staticmethod
    def data(table_id: str) -> str:
        return f'CREATE TABLE {table_id} (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'date TEXT NOT NULL, ' \
            'price REAL NOT NULL, ' \
            'target REAL NOT NULL, ' \
            'value REAL NOT NULL, ' \
            'recommend REAL NOT NULL, ' \
            'side TEXT NOT NULL, ' \
            'base REAL NOT NULL, ' \
            'base_fee REAL NOT NULL, ' \
            'base_total REAL NOT NULL, ' \
            'base_prev REAL NOT NULL, ' \
            'quote REAL NOT NULL, ' \
            'quote_fee REAL NOT NULL, ' \
            'quote_total REAL NOT NULL, ' \
            'quote_prev REAL NOT NULL, ' \
            'period INTEGER NOT NULL)'


class QueryRaw(object):
    @staticmethod
    def select(cols: str, table: str) -> str:
        return f'SELECT {cols} FROM {table}'

    @staticmethod
    def select_where(cols: str, table: str, cond: str) -> str:
        return f'SELECT {cols} FROM {table} WHERE {cond}'

    @staticmethod
    def insert(table: str, cols: str, vals: str) -> str:
        return f'INSERT INTO {table} ({cols}) VALUES {vals}'

    @staticmethod
    def update_where(table: str, cols: str, cond: str) -> str:
        return f'UPDATE {table} SET {cols} WHERE {cond}'

    @staticmethod
    def delete_where(table: str, cond: str) -> str:
        return f'DELETE FROM {table} WHERE {cond}'

    @staticmethod
    def drop(table: str) -> str:
        return f'DROP TABLE {table}'


class QueryUser(object):
    @property
    def table(self) -> str:
        return 'user'

    @property
    def cols(self) -> str:
        return 'uuid, name, password, '\
            'key, secret, passphrase, '\
            'interface, websocket, currency, theme'

    @property
    def vals(self) -> str:
        return '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    def select(self, cols: str, cond: str = None) -> str:
        if cond is None:
            return QueryRaw.select(cols, self.table)
        else:
            return QueryRaw.select_where(cols, self.table, cond)

    def insert(self) -> str:
        return QueryRaw.insert(self.table, self.cols, self.vals)

    def update(self, cols: str, cond: str) -> str:
        return QueryRaw.update_where(self.table, cols, cond)

    def delete(self, cond: str) -> str:
        return QueryRaw.delete_where(self.table, cond)

    def drop(self) -> str:
        return QueryRaw.drop(self.table)


class QueryStrategy(object):
    @property
    def table(self) -> str:
        return 'strategy'

    @property
    def cols(self) -> str:
        return 'product, name, frequency, principle, rate, period, alive'

    @property
    def vals(self) -> str:
        return '(?, ?, ?, ?, ?, ?, ?)'

    def select(self, cols: str, cond: str = None) -> str:
        if cond is None:
            return QueryRaw.select(cols, self.table)
        else:
            return QueryRaw.select_where(cols, self.table, cond)

    def insert(self) -> str:
        return QueryRaw.insert(self.table, self.cols, self.vals)

    def update(self, cols: str, cond: str) -> str:
        return QueryRaw.update_where(self.table, cols, cond)

    def delete(self, cond: str) -> str:
        return QueryRaw.delete_where(self.table, cond)

    def drop(self) -> str:
        return QueryRaw.drop(self.table)


class QueryDatabase(object):
    def __init__(self):
        self.__schema = QuerySchema()
        self.__raw = QueryRaw()
        self.__user = QueryUser()
        self.__strategy = QueryStrategy()

    @property
    def schema(self) -> QuerySchema:
        return self.__schema

    @property
    def raw(self) -> QueryRaw:
        return self.__raw

    @property
    def user(self) -> QueryUser:
        return self.__user

    @property
    def strategy(self) -> QueryStrategy:
        return self.__strategy


class SQLiteMeta(object):
    def __init__(self, path: str = None, name: str = None):
        self.__path = path or f'{environ["PWD"]}/instance'
        self.__name = name or 'database.sqlite'

    @property
    def master(self) -> str:
        return 'sqlite_master'

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def filepath(self) -> str:
        return join(self.__path, self.__name)


class SQLiteDatabase(object):
    def __init__(self, meta: SQLiteMeta = None):
        self.__meta = meta or SQLiteMeta()

    @property
    def meta(self) -> SQLiteMeta:
        return self.__meta

    @meta.setter
    def meta(self, value: SQLiteMeta):
        self.__meta = value

    @property
    def tables(self) -> list:
        tables = []
        query = 'SELECT tbl_name ' \
                f'FROM {self.meta.master} ' \
                'WHERE type = "table"'
        for row in self.fetchall(query):
            tables.append(row[0])
        return tables

    @property
    def databases(self) -> list:
        databases = []
        extensions = ['db', 'database', 'sqlite']
        for entry in scandir(f'{self.meta.path}'):
            name, ext = entry.name.split('.')
            if entry.is_file() and ext in extensions:
                databases.append(name)
        return databases

    def connect(self) -> Connection:
        return connect(self.meta.filepath)

    def execute(self, query: str, params: Iterable[Any] = None) -> None:
        if not params:
            params = tuple()
        database = self.connect()
        database.execute(query, params)
        database.commit()
        database.close()

    def executemany(self, query: str, params: Iterable[Any] = None) -> None:
        if not params:
            params = tuple()
        database = self.connect()
        database.executemany(query, params)
        database.commit()
        database.close()

    def fetchone(self, query: str, params: Iterable[Any] = None) -> Row:
        if not params:
            params = tuple()
        database = self.connect()
        database.row_factory = Row
        cursor = database.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        database.close()
        return row

    def fetchall(self, query: str, params: Iterable[Any] = None) -> list[Row]:
        if not params:
            params = tuple()
        database = self.connect()
        database.row_factory = Row
        cursor = database.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        database.close()
        return rows

    def plug(self, callback: object, *args: list, **kwargs: dict) -> object:
        connection = self.connect()
        result = callback(connection, *args, **kwargs)
        connection.close()
        return result

    def drop(self, filepath: str = None) -> bool:
        try:
            remove(filepath or self.meta.filepath)
            return True
        except (FileNotFoundError,):
            return False
