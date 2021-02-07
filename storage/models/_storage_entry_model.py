from ... import Model
from dataclasses import dataclass

@dataclass
class StorageEntryModel(Model):
    id: str
    partition_key: str
    data: dict
    etag: str = '*'