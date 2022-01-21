from typing import Union
from .... import Model
from dataclasses import dataclass

@dataclass
class DatabaseEntryModel(Model):
    data: dict
    partition_key: Union[str, int]
    etag: str = '*'
    id: Union[str, int] = None