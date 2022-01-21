from abc import abstractmethod
from .models import DatabaseEntryModel
from typing import Union, Dict, Any, List

class DatabaseOperations():
    @abstractmethod
    def get(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int]) -> DatabaseEntryModel:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int]) -> List[DatabaseEntryModel]:
        raise NotImplementedError()

    @abstractmethod
    def insert(self, db_entry: DatabaseEntryModel) -> Union[str, int]:
        raise NotImplementedError()
    
    @abstractmethod
    def insert_or_update(self, db_entry: DatabaseEntryModel) -> Union[str, int]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, db_entry: DatabaseEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: Union[str, int], partition_key: Union[str, int]):
        raise NotImplementedError()
