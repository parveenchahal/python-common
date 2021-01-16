from common.storage import Storage
from common import Model
from .models import StorageEntryModel
from threading import RLock


class InMemoryDictStorage(Storage):

    _dict: dict
    _lock: RLock

    def __init__(self):
        self._lock = RLock()
        self._dict = {}

    def get(self, id: str, partition_key: str, model_for_data: Model) -> StorageEntryModel:
        with self._lock:
            return self._dict[partition_key][id]
    
    def add_or_update(self, storage_entry: StorageEntryModel):
        with self._lock:
            self._dict[storage_entry.partition_key][storage_entry.id] = storage_entry

    def delete(self, id: str, partition_key: str):
        del self._dict[partition_key][id]