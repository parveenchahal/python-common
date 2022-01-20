from typing import Union
from .... import Model
from dataclasses import dataclass

@dataclass
class DatabaseEntryModel(Model):
    data: dict
    partition_key: Union[str, int, float]
    etag: str = '*'
    id: str = None