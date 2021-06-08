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
import json
import os
import scrypt


def shash(password: str) -> str:
    salt = os.urandom(64)
    n, r, p, dklen = 16384, 8, 1, 64
    dk = scrypt.hash(password, salt, n, r, p, dklen)
    return f'{n}${r}${p}${dklen}${salt.hex()}${dk.hex()}'


def sverify(password: str, hashed: str) -> bool:
    n, r, p, dklen, salt, dk = hashed.split('$')
    tk = scrypt.hash(
        password,
        bytes.fromhex(salt),
        int(n), int(r), int(p),
        int(dklen)
    ).hex()
    return True if tk == dk else False


def ssalt(hashed: str) -> str:
    _, _, _, _, salt, _ = hashed.split('$')
    return salt


def sencrypt(data: object, password: str) -> bytes:
    payload = json.dumps(data).encode()
    return scrypt.encrypt(payload, password)


def sdecrypt(data: bytes, password: str) -> object:
    payload = scrypt.decrypt(data, password)
    return json.loads(payload)
