from logging import Logger
from operator import le
from typing import Union, Dict, Any, List
from uuid import uuid4
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from ..models import DatabaseEntryModel
from .._abstract_database_operations import DatabaseOperations
from ._mongodb_database import MongoDBDatabase
from .... import exceptions

class CollectionOperations(DatabaseOperations):

    _logger: Logger
    _collection: Collection
    _ID_KEY = '_id'
    _PARTITION_KEY = '_partitionKey'
    _ETAG_KEY = '_etag'

    def __init__(self, logger: Logger, name: str, db: MongoDBDatabase) -> None:
        self._logger = logger
        self._collection = db.get_collection(name)

    def get(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int] = None) -> DatabaseEntryModel:
        res = self.get_all(filter, partition_key)
        if res and len(res) > 0:
            return res[0]
        return None

    def _parse_response(self, res: List[dict]) -> List[DatabaseEntryModel]:
        parsed_res = []
        for r in res:
            id = str(r.pop(self._ID_KEY))
            pkey = r.pop(self._PARTITION_KEY, None)
            etag = r.pop(self._ETAG_KEY, '*')
            e = DatabaseEntryModel(r, pkey, etag, id)
            parsed_res.append(e)
        return parsed_res

    def get_all(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int] = None) -> List[DatabaseEntryModel]:
        if isinstance(filter, (str, int)):
            filter = {self._ID_KEY: filter}
        elif isinstance(filter, dict):
            filter = dict(filter)
        else:
            raise TypeError('Unknown type')
        filter[self._PARTITION_KEY] = partition_key
        res = self._collection.find(filter)
        res = list(res)
        if len(res) > 0:
            res = self._parse_response(res)
            return res
        return None

    def insert(self, db_entry: DatabaseEntryModel):
        document = dict(db_entry.data)
        if db_entry.id is None:
            document[self._ID_KEY] = str(uuid4())
        else:
            document[self._ID_KEY] = db_entry.id
        if db_entry.partition_key is not None:
            document[self._PARTITION_KEY] = db_entry.partition_key
        if db_entry.etag is not None:
            document[self._ETAG_KEY] = db_entry.etag
        else:
            document[self._ETAG_KEY] = '*'
        try:
            self._collection.insert_one(document)
        except DuplicateKeyError as e:
            self._logger.exception(e)
            raise exceptions.KeyAlreadyExist('Record already exist')

    def update(self, db_entry: DatabaseEntryModel):
        if db_entry.id is None:
            raise ValueError('DatabaseEntryModel.id can not be None')
        document = dict(db_entry.data)
        if db_entry.partition_key is not None:
            document[self._PARTITION_KEY] = db_entry.partition_key
        if db_entry.etag is not None:
            document[self._ETAG_KEY] = db_entry.etag
        else:
            document[self._ETAG_KEY] = '*'
        try:
            self._collection.update_one({self._ID_KEY: db_entry.id}, {'$set': db_entry.data})
        except DuplicateKeyError as e:
            self._logger.exception(e)
            raise exceptions.KeyAlreadyExist('Record already exist')


    def delete(self, filter: Union[str, Dict[str, Any]], partition_key: str):
        return super().delete(filter, partition_key)