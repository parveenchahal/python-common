from abc import abstractmethod
from .models import StorageEntryModel
from typing import List

class Storage():
    @abstractmethod
    def get(self, id: str, partition_key: str) -> StorageEntryModel:
        raise NotImplementedError()
    
    @abstractmethod
    def add_or_update(self, storage_entry: StorageEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str, partition_key: str):
        raise NotImplementedError()
