from flask import g
from teleprint_me.proxy.client import ProxyClient
from teleprint_me.proxy.database import (
    ProxyData,
    ProxyDatabase,
    ProxyInterface,
    ProxyStrategy,
    ProxyUser,
)

database = ProxyDatabase(ProxyUser(), ProxyInterface(), ProxyStrategy(), ProxyData())
client = ProxyClient(g.client)
