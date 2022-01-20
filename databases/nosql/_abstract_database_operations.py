from abc import abstractmethod
from .models import DatabaseEntryModel
from typing import Union, Dict, Any, List

class DatabaseOperations():
    @abstractmethod
    def get(self, filter: Union[str, Dict[str, Any]], partition_key: Union[str, int, float]) -> DatabaseEntryModel:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int] = None) -> List[DatabaseEntryModel]:
        raise NotImplementedError()
    
    @abstractmethod
    def insert(self, db_entry: DatabaseEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def update(self, filter: Union[str, Dict[str, Any]], db_entry: DatabaseEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, filter: Union[str, Dict[str, Any]], partition_key: Union[str, int, float]):
        raise NotImplementedError()
