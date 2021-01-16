from base64 import b64decode as _b64decode
from common.utils import string_to_bytes, parse_json
from common import Model
from typing import Dict
from dataclasses import dataclass

@dataclass
class Certificate(Model):
    private_key: bytes
    certificate: bytes

    @staticmethod
    def from_json_string(cls, json_data: str):
        d:Dict[str] = parse_json(json_data)
        bd = {
            'private_key': _b64decode(string_to_bytes(d['key'])),
            'certificate': _b64decode(string_to_bytes(d['crt']))
        }
        return cls(**bd)