from ledger.core import generate

import os

SECRET_KEY = generate.gbytes()
MONGO_URI = os.environ.get('MONGO_URI')
