import base64
import json
import hashlib

import M2Crypto
from binascii import hexlify


class AuthorizationProvider:
    __doc__ = """"""

    def __init__(self, key_path, passphrase=None):
        with open(key_path, 'rb') as f:
            self._key = M2Crypto.RSA.load_key_string(f.read())
        pass

    def get_sign(self, data):
        data_dump = json.dumps(data).replace(" ", "").encode()
        sha = hashlib.sha1(data_dump)
        sign = self._key.private_encrypt(hexlify(sha.digest()), M2Crypto.RSA.pkcs1_padding)
        return self._format(sign)

    def _format(self, sign):
        return base64.b64encode(sign).decode("ascii").replace('+', '-').replace('/', '_').rstrip('=')
