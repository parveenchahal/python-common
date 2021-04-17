import json
from base64 import b64encode, b64decode
from typing import Any, TypeVar
T = TypeVar('T')

def bytes_to_string(b: bytes, encoding='UTF-8') -> str:
    return b.decode(encoding, errors='strict')

def string_to_bytes(s: str, encoding='UTF-8') -> bytes:
    return s.encode(encoding, errors='strict')

def encode_base64(data, altchars: bytes = None, encoding='UTF-8', remove_padding: bool = False):
    if isinstance(data, bytes):
        b64e = b64encode(data, altchars=altchars)
        if remove_padding:
            b64e = b64e.rstrip(b'=')
        return b64e
    if isinstance(data, str):
        b64e = b64encode(string_to_bytes(data, encoding), altchars=altchars)
        if remove_padding:
            b64e = b64e.rstrip(b'=')
        return bytes_to_string(b64e, encoding)
    raise ValueError("Format is not supported")

def decode_base64(data, altchars: bytes=None, encoding='UTF-8'):
    if isinstance(data, bytes):
        return b64decode(data, altchars=altchars)
    if isinstance(data, str):
        return bytes_to_string(b64decode(string_to_bytes(data, encoding), altchars=altchars), encoding)
    raise ValueError("Format is not supported")

def parse_json(json_string: str):
    return json.loads(json_string)

def json_to_obj(cls: T, json_string: str) -> T:
    j = parse_json(json_string)
    return cls(**j)

def dict_to_obj(cls: T, d: dict) -> T:
    keys = list(cls.__dataclass_fields__)
    new_dict = {}
    for key in keys:
        if key in d:
            new_dict[key] = d[key]
    return cls(**new_dict)

def to_json_string(d: dict) -> str:
    return json.dumps(d)
