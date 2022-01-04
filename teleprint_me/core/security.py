from jwcrypto import jwk
from jwcrypto import jws
from jwcrypto.common import json_encode
from jwcrypto.common import json_decode

import base64
import hmac
import json
import os
import random
import scrypt
import string
import time
import uuid

TIMEOUT: int = 3600


class Generate(object):
    """wrapper class for generating random bytes and strings"""

    @property
    def size(self) -> int:
        return 64

    @property
    def symbols(self) -> str:
        return f'_{string.ascii_letters}{string.digits}'

    def bytes(self, size: int = None) -> bytes:
        if size is None:
            size = self.size
        return base64.urlsafe_b64encode(os.urandom(size))

    def string(self, size: int = None) -> str:
        return self.bytes(size).decode('utf-8')

    def identifer(self, size: int = None) -> str:
        if size is None:
            size = self.size
        prefix = random.SystemRandom().choice(string.ascii_letters)
        body = (''.join(
                random.SystemRandom().choice(self.symbols)
                for _ in range(size - 1)
                ))
        return f'{prefix}{body}'


class Scrypt(object):
    """wrapper class for handling scrypt functions"""

    @staticmethod
    def hash(password: str) -> str:
        """return a hashed password as str"""
        salt = os.urandom(64)
        n, r, p, dklen = 16384, 8, 1, 64
        dk = scrypt.hash(password, salt, n, r, p, dklen)
        return f'{n}${r}${p}${dklen}${salt.hex()}${dk.hex()}'

    @staticmethod
    def verify(data: str, password: str) -> bool:
        """return True if hashed password is verified else False"""
        n, r, p, dklen, salt, dk = data.split('$')
        tk = scrypt.hash(
            password,
            bytes.fromhex(salt),
            int(n), int(r), int(p),
            int(dklen)
        ).hex()
        return hmac.compare_digest(bytes.fromhex(tk), bytes.fromhex(dk))

    @staticmethod
    def salt(hashed: str) -> str:
        """return the salt from the hashed password"""
        _, _, _, _, salt, _ = hashed.split('$')
        return salt

    @staticmethod
    def encrypt(data: object, password: str) -> bytes:
        """return the encrypted data object as bytes using password"""
        payload = json.dumps(data).encode()
        return scrypt.encrypt(payload, password)

    @staticmethod
    def decrypt(data: bytes, password: str) -> object:
        """return decrypted bytes as object using password"""
        payload = scrypt.decrypt(data, password)
        return json.loads(payload)


def serialize(sig: str) -> str:
    """return a JWT token"""

    hdr = json_decode(sig)
    return f'{hdr["protected"]}.{hdr["payload"]}.{hdr["signature"]}'


def deserialize(hdr: str) -> str:
    """return a JWT signature"""

    try:
        protected, payload, signature = hdr.split('.')
        sig = json_encode({
            'payload': payload,
            'protected': protected,
            'signature': signature
        })
        return sig
    except (ValueError,):
        return str()


class Policy(object):
    """JSON Web Token: https://tools.ietf.org/html/rfc7519"""

    def __init__(self, aud=None):
        self.__iss = 'https://teleprint.me'
        self.__sub = 'https://github.com/teleprint-me/teleprint-me'
        self.__aud = Generate.identifer() if aud is None else aud
        self.__jti = str(uuid.uuid4())
        self.__iat = int(time.time())
        self.__exp = self.__iat + TIMEOUT

    @property
    def iss(self) -> str:
        return self.__iss

    @property
    def sub(self) -> str:
        return self.__sub

    @property
    def aud(self) -> str:
        return self.__aud

    @aud.setter
    def aud(self, value: str):
        self.__aud = value

    @property
    def jti(self) -> str:
        return str(self.__jti)

    @property
    def iat(self) -> int:
        return self.__iat

    @property
    def exp(self) -> int:
        return self.__exp

    @property
    def expired(self):
        now = int(time.time())
        if (now - self.iat) < TIMEOUT:
            return False
        return True

    @property
    def claims(self) -> dict:
        return {
            'iss': self.iss,
            'sub': self.sub,
            'aud': self.aud,
            'jti': self.jti,
            'iat': self.iat,
            'exp': self.exp
        }

    def verify(self, claims):
        return claims == self.claims


class Gaurd(object):
    """wrapper class for handling json web tokens"""

    def __init__(self, kty=None, size=None, alg=None):
        self.__kty = 'oct' if kty is None else kty
        self.__size = 256 if size is None else size
        self.__alg = 'HS256' if alg is None else alg
        self.__key = jwk.JWK.generate(kty=self.__kty, size=self.__size)
        self.__header = {'alg': self.__alg, 'kid': self.__key.thumbprint()}
        self.__tok = None
        self.__sig = None
        self.__hdr = None
        self.__pol = None

    @property
    def tok(self):
        return self.__tok

    @property
    def sig(self):
        return self.__sig

    @property
    def hdr(self):
        return self.__hdr

    @property
    def pol(self):
        return self.__pol

    def sign(self, policy: Policy = None) -> str:
        """return a signed JWT header token"""

        self.__pol = Policy() if policy is None else policy
        self.__tok = jws.JWS(json_encode(self.__pol.claims))
        self.__tok.add_signature(
            self.__key,
            alg=None,
            protected=json_encode(self.__header)
        )
        self.__sig = self.__tok.serialize()
        self.__hdr = serialize(self.__sig)
        return self.__hdr

    def verify(self, hdr: str) -> bool:
        """return JWT header verification as a bool"""

        try:
            sig = deserialize(hdr)
            self.__tok.deserialize(sig)
            self.__tok.verify(self.__key)
            return True
        except (jws.InvalidJWSSignature, jws.InvalidJWSObject,):
            return False
