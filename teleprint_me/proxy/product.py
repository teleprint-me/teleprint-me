from dataclasses import dataclass, field

from teleprint_me import proxy
from teleprint_me.core import sqlite


@dataclass(frozen=True)
class Data(object):
    fills: list[dict]
    transfers: list[dict]

    def list_(self) -> tuple[dict]:
        return tuple(self.fills + self.transfers)

    def sorted_(self) -> tuple[dict]:
        return tuple(sorted(self.list_(), key=lambda item: item.get("created_at")))

    def reversed_(self) -> tuple[dict]:
        data = list(self.sorted_())
        data.reverse()
        return tuple(data)


class Product(object):
    def __init__(self, name: str):
        strategy = proxy.database.strategy.get(name)
        fills = proxy.client.get_fills(strategy.product)
        account, transfers = proxy.client.get_transfers(strategy.base)

        self.__strategy: sqlite.Strategy = strategy
        self.__account: dict = account
        self.__data: Data = Data(fills, transfers)

    @property
    def data(self) -> Data:
        return self.__data

    @property
    def account(self) -> dict:
        return self.__account

    @property
    def strategy(self) -> sqlite.Strategy:
        return self.__strategy


# if Row.type is withdraw, then Row.period is -1
# if Row.type is deposit, then Row.period is 0
# if Row.type is buy or sell, then Row.period is >= 1
@dataclass
class Row(object):
    date: str = str()
    period: int = int()
    price: float = float()
    target: float = float()
    value: float = float()
    recommend: float = float()
    side: str = str()
    base: float = float()
    base_fee: float = float()
    base_total: float = float()
    base_prev: float = float()
    quote: float = float()
    quote_fee: float = float()
    quote_total: float = float()
    quote_prev: float = float()

    @property
    def istransfer(self) -> bool:
        return self.side in ("deposit", "withdraw")

    @property
    def istrade(self) -> bool:
        return self.side in ("buy", "sell")


@dataclass
class Builder(object):
    product: Product
    row: Row = None
    rows: list[Row] = field(default_factory=list)
    base_prev: float = float()
    quote_prev: float = float()

    def inc_period(self):
        self.product.strategy.period += 1

    def dec_period(self):
        self.product.strategy.period -= 1

    def set_date(self, data: dict):
        self.row.date = data.get("created_at")

    def set_transfer_data(self, data):
        self.row.side = data.get("type")
        self.row.period = -1 if data.get("type") == "withdraw" else int()
        self.row.base = float(data.get("amount"))
        self.row.base_prev = self.base_prev

    def set_transfer_fee(self, data):
        try:
            self.row.base_fee = float(data["details"]["fee"])
        except (KeyError,):
            self.row.base_fee = float()

    def set_transfer_base_prev(self):
        if self.row.side == "deposit":
            self.base_prev += self.row.base
        elif self.row.side == "withdraw":
            if (self.base_prev - self.row.base) > 0:
                self.base_prev -= self.row.base

    def set_transfer_base_total(self):
        self.row.base_total = self.base_prev

    def set_transfer(self, data):
        self.set_transfer_data(data)
        self.set_transfer_fee(data)
        self.set_transfer_base_prev()
        self.set_transfer_base_total()

    def set_trade_data(self, data: dict):
        self.row.period = self.product.strategy.period
        self.row.target = proxy.database.strategy.get_target(self.product.strategy)
        self.row.price = float(data.get("price"))
        self.row.value = self.row.price * self.base_prev
        self.row.recommend = self.row.target - self.row.value
        self.row.side = data.get("side")
        self.row.base = float(data.get("size"))
        self.row.quote = self.row.price * self.row.base
        self.row.base_fee = float(data.get("fee"))
        self.row.base_prev = self.base_prev

    def set_trade_prev(self):
        if self.row.side == "buy":
            self.base_prev += self.row.base
            self.quote_prev += self.row.quote
        if self.row.side == "sell":
            self.base_prev -= self.row.base
            self.quote_prev -= self.row.quote

    def set_trade_total(self):
        self.row.base_total = self.base_prev
        self.row.quote_total = self.quote_prev

    def set_trade(self, data):
        self.set_trade_data(data)
        self.set_trade_prev()
        self.set_trade_total()

    def build(self) -> list[Row]:
        for data in self.product.data.sorted_():
            self.inc_period()
            self.row = Row()
            self.set_date(data)
            if "type" in data:
                self.dec_period()
                self.set_transfer(data)
            if "side" in data:
                self.set_trade(data)
            self.rows.append(self.row)
        return self.rows


def get_builder(name: str) -> Builder:
    return Builder(Product(name))


def get_rows(name: str) -> list[Row]:
    return Builder(Product(name)).build()
