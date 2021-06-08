# Ledger - A web application to track cryptocurrency investments
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
