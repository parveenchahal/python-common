import os, json
from datetime import datetime, timedelta
from time import sleep
from typing import TypeVar, Union
from io import BytesIO
from base64 import b64encode, b64decode

T = TypeVar('T')

def bytes_to_string(b: bytes, encoding='UTF-8') -> str:
    return b.decode(encoding, errors='strict')

def string_to_bytes(s: str, encoding='UTF-8') -> bytes:
    return s.encode(encoding, errors='strict')

def encode_base64(
    data, altchars: bytes = None, encoding='UTF-8', remove_padding: bool = False):
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
        return bytes_to_string(
            b64decode(string_to_bytes(data, encoding), altchars=altchars), encoding)
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

def chunked(content: Union[bytes, BytesIO], chuck_size: int = 1024):
    if isinstance(content, bytes):
        bytes_io = BytesIO(content)
    else:
        bytes_io = content
    try:
        while True:
            chunk = bytes_io.read(chuck_size)
            if not chunk:
                break
            yield chunk
    finally:
        bytes_io.close()

def wait_until(callback, timeout: timedelta, frequency: timedelta = timedelta(seconds=10)):
    now = datetime.utcnow()
    endtime = now + timeout
    while datetime.utcnow() <= endtime:
        if callback():
            return
        sleep(frequency.total_seconds())
    raise TimeoutError()

class TempChangeDir(object):
    def __init__(self, dir) -> None:
        self._prev = os.getcwd()
        self._new = dir

    def __enter__(self):
        os.chdir(self._new)

    def __exit__(self, *args, **kwargs):
        os.chdir(self._prev)
