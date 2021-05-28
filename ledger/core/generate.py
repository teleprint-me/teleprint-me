from base64 import urlsafe_b64encode
from os import urandom
from random import SystemRandom
from string import digits as DIGITS
from string import ascii_letters as LETTERS

SIZE = 64
SYMBOLS = f'_{LETTERS}{DIGITS}'


def gbytes(size: int = None) -> bytes:
    if size is None:
        size = SIZE
    data = urandom(size)
    return urlsafe_b64encode(data)


def gstring(size: int = None) -> str:
    return gbytes(size).decode('utf-8')


def gidentifer(size=None):
    if size is None:
        size = SIZE
    prefix = SystemRandom().choice(LETTERS)
    body = ''.join(SystemRandom().choice(SYMBOLS) for _ in range(size - 1))
    return f'{prefix}{body}'
