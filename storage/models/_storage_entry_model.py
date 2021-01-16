from common import Model
from dataclasses import dataclass

@dataclass
class StorageEntryModel(Model):
    id: str
    data: Model
    partition_key: str
    etag: str = '*'