from flask import g
from teleprint_me.proxy.client import ProxyClient
from teleprint_me.proxy.database import (
    ProxyData,
    ProxyDatabase,
    ProxyInterface,
    ProxyStrategy,
    ProxyUser,
)

client = ProxyClient(g.client) if g.client else None
database = ProxyDatabase(ProxyUser(), ProxyInterface(), ProxyStrategy(), ProxyData())
