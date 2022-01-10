from base64 import b64decode as _b64decode
from ...utils import parse_json
from ... import Model
from typing import Dict
from dataclasses import dataclass

@dataclass
class Certificate(Model):

    certificate: bytes
    private_key: bytes = None
    

    @staticmethod
    def from_json_string(cls, json_data: str):
        d: Dict[str] = parse_json(json_data)
        bd = {
            'private_key': _b64decode(d['key']),
            'certificate': _b64decode(d['crt'])
        }
        return cls(**bd)