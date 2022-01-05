from dataclasses import dataclass, field

from coinbase_pro.client import Client
from peewee import ModelSelect
from teleprint_me.core import proxy, sqlite

header: list[str] = [
    "Date",
    "Period",
    "Price",
    "Target",
    "Value",
    "Recommend",
    "Side",
    "Fiat",
    "Fiat Fee",
    "Fiat Total",
    "Size",
    "Size Fee",
    "Size Total",
]


class Strategy(object):
    def __init__(self, name: str):
        self.__strategy = sqlite.get_strategy(name)

    def __repr__(self) -> str:
        return f"Strategy({self.name}, len={len(self.__strategy.datum)})"

    def __str__(self) -> str:
        return self.__strategy.name

    def __len__(self) -> int:
        return len(self.__strategy.datum)

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    @property
    def model(self) -> sqlite.Strategy:
        return self.__strategy

    @property
    def name(self) -> str:
        return self.__strategy.name

    @property
    def base(self) -> str:
        return self.__strategy.base

    @property
    def quote(self) -> str:
        return self.__strategy.quote

    @property
    def product(self) -> str:
        return self.__strategy.product

    @property
    def type_(self) -> str:
        return self.__strategy.type_

    @property
    def frequency(self) -> int:
        return {"daily": 365, "weekly": 52, "monthly": 12}.get(
            self.__strategy.frequency, 12
        )

    @property
    def principal(self) -> float:
        return float(self.__strategy.principal)

    @property
    def yield_(self) -> float:
        return float(self.__strategy.yield_)

    @property
    def rate(self) -> float:
        return 1 + (self.yield_ / self.frequency)

    @property
    def period(self) -> int:
        return int(self.__strategy.period)

    @period.setter
    def period(self, value: str):
        if 0 > int(value):
            raise AttributeError("Period must be greater than or equal to 1")
        self.__strategy.period = str(value)

    @property
    def target(self) -> float:
        if self.period == 1:
            return self.principal
        if self.__strategy.type_ == "value_average":
            return self.principal * self.period * (self.rate ** self.period)
        return self.principal * self.period

    @property
    def datum(self) -> ModelSelect:
        return self.__strategy.datum


@dataclass(frozen=True)
class Data(object):
    fills: list[dict]
    withdrawals: list[dict]
    deposits: list[dict]

    def __len__(self) -> int:
        return len(self.fills + self.withdrawals + self.deposits)

    def list_(self) -> tuple[dict]:
        return tuple(self.fills + self.withdrawals + self.deposits)

    def sorted_(self) -> tuple[dict]:
        return tuple(sorted(self.list_(), key=lambda item: item["created_at"]))

    def reversed_(self) -> tuple[dict]:
        data = list(self.sorted_())
        data.reverse()
        return tuple(data)


class Product(object):
    def __init__(self, client: Client, name: str):
        strategy = Strategy(name)
        fills = proxy.get_fills(client, strategy.product)
        _, withdrawals = proxy.get_withdrawals(client, strategy.product)
        account, deposits = proxy.get_deposits(client, strategy.product)

        self.__strategy: Strategy = strategy
        self.__account: dict = account
        self.__data: Data = Data(fills, withdrawals, deposits)

    def __repr__(self) -> str:
        return f"Product({self.strategy.product}, txs={len(self.data)})"

    def __str__(self) -> str:
        return self.strategy.product

    def __len__(self) -> int:
        return len(self.data)

    def __eq__(self, o: object) -> bool:
        return self.strategy == o.strategy

    @property
    def base(self) -> str:
        return self.__strategy.base

    @property
    def quote(self) -> str:
        return self.__strategy.quote

    @property
    def id_(self) -> str:
        return self.__strategy.product

    @property
    def data(self) -> Data:
        return self.__data

    @property
    def account(self) -> dict:
        return self.__account

    @property
    def strategy(self) -> Strategy:
        return self.__strategy


# if Row.type is deposit or withdraw, then Row.period is type str of len 1
# if Row.type is buy or sell, then Row.period is type int
@dataclass
class Row(object):
    date: str = str()
    period: object = None
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
        return self.side in ["deposit", "withdraw"]

    @property
    def istrade(self) -> bool:
        return self.side in ["buy", "sell"]


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
        self.row.date = data["created_at"]

    def set_transfer_data(self, data):
        self.row.side = data["type"]
        self.row.period = data["type"][0].upper()
        self.row.quote = float(data["amount"])
        self.row.quote_prev = self.quote_prev

    def set_transfer_fee(self, data):
        try:
            self.row.quote_fee = float(data["details"]["fee"])
        except (KeyError,):
            self.row.quote_fee = float()

    def set_transfer_quote_prev(self):
        if self.row.side == "deposit":
            self.quote_prev += self.row.quote
        elif self.row.side == "withdraw":
            if self.quote_prev - self.row.quote > 0:
                self.quote_prev -= self.row.quote

    def set_transfer_quote_total(self):
        self.row.quote_total = self.quote_prev

    def set_transfer(self, data):
        self.set_transfer_data(data)
        self.set_transfer_fee(data)
        self.set_transfer_quote_prev()
        self.set_transfer_quote_total()

    def set_trade_data(self, data: dict):
        self.row.period = self.product.strategy.period
        self.row.target = self.product.strategy.target
        self.row.price = float(data["price"])
        self.row.value = self.row.price * self.quote_prev
        self.row.recommend = self.product.strategy.target - self.row.value
        self.row.side = data["side"]
        self.row.quote = float(data["size"])
        self.row.base = self.row.price * self.row.quote
        self.row.base_fee = float(data["fee"])
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


def get_builder(client: Client, name: str) -> Builder:
    return Builder(Product(client, name))


def get_rows(client: Client, name: str) -> list[Row]:
    return Builder(Product(client, name)).build()
