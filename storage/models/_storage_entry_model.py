from ... import Model
from dataclasses import dataclass

@dataclass
class StorageEntryModel(Model):
    id: str
    data: dict
    partition_key: str
    etag: str = '*'