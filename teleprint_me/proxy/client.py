from coinbase_pro.client import CoinbasePro


class ProxyBase:
    def __init__(self, client: CoinbasePro):
        self.__client = client

    @property
    def client(self) -> CoinbasePro:
        return self.__client


class ProxyProduct(ProxyBase):
    def ids(self) -> list[str]:
        return [product.get("id") for product in self.client.product.list()]


class ProxyAccount(ProxyBase):
    def balance(self, floor: float = None) -> list[dict]:
        floor = float(floor) if floor else float()
        return [
            account
            for account in self.client.account.list()
            if floor < float(account.get("balance", int()))
        ]

    def type(self, account: dict, tx_type: str) -> list[dict]:
        return [
            tx
            for tx in self.client.transfer.list()
            if account.get("id") == tx.get("account_id") and tx.get("type") == tx_type
        ]

    def id(self, account: dict) -> list[dict]:
        return [
            tx
            for tx in self.client.transfer.list()
            if account.get("id") == tx.get("account_id")
        ]


class ProxyFilter:
    def __init__(self, client: CoinbasePro):
        self.product = ProxyProduct(client)
        self.account = ProxyAccount(client)


class ProxyClient(ProxyBase):
    def __init__(self, client: CoinbasePro):
        super(ProxyClient, self).__init__(client)
        self.__filter = ProxyFilter(client)

    @property
    def filter(self) -> ProxyFilter:
        return self.__filter

    def get_account(self, currency: str) -> dict:
        try:
            return [
                account
                for account in self.client.account.list()
                if account.get("currency") == currency
            ][0]
        except (IndexError,):
            return dict()

    def get_transfers(self, currency: str) -> list[dict, list[dict]]:
        account = self.get_account(currency)
        txs = self.filter.account.id(account)
        return [account, txs]

    def get_withdrawals(self, currency: str) -> list[dict, list[dict]]:
        account = self.get_account(currency)
        withdrawals = self.filter.account.type(account, "withdraw")
        return [account, withdrawals]

    def get_deposits(self, currency: str) -> list[dict, list[dict]]:
        account = self.get_account(currency)
        deposits = self.filter.account.type(account, "deposit")
        return [account, deposits]

    def get_price(self, product_id: str) -> dict:
        return self.client.product.ticker(product_id)

    def get_fills(self, product_id: str) -> list[dict]:
        return self.client.order.fills({"product_id": product_id})

    def get_order(self) -> dict:
        return {}

    def post_order(self, data: dict) -> dict:
        return self.client.order.post(data)
