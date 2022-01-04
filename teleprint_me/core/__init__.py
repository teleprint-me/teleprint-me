from datetime import datetime
from dateutil import parser

from teleprint_me.core.database import settings_path
from teleprint_me.core.security import Generate
from teleprint_me.core.security import Scrypt

import json

generate = Generate()
scrypt = Scrypt()


#
# Settings
#
def get_settings() -> dict:
    with open(settings_path, 'r') as file:
        return json.load(file)


def set_settings(data: dict):
    with open(settings_path, 'w') as file:
        file.write(json.dump(data))


#
# Datetime
#
def iso_to_datetime(data: list[dict]) -> list[dict]:
    for item in data:
        item['timestamp']: datetime = parser.parse(item['timestamp'])
    return data


def datetime_to_iso(data: list[dict]) -> list[dict]:
    for item in data:
        item['timestamp']: str = item['timestamp'].isoformat()
    return data
