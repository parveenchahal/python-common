from logging import Logger
from typing import Union, Dict, List
from uuid import uuid4
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from ..models import DatabaseEntryModel
from .._abstract_database_operations import DatabaseOperations
from ._mongodb_database import MongoDBDatabase
from ...errors import RecordAlreadyExist, RecordNotFound, RecordUpdateFailed, DatabaseOperationFailed

class CollectionOperations(DatabaseOperations):

    _logger: Logger
    _collection: Collection
    _ID_KEY = '_id'
    _PARTITION_KEY = '_partitionKey'
    _ETAG_KEY = '_etag'

    def __init__(self, logger: Logger, name: str, db: MongoDBDatabase) -> None:
        self._logger = logger
        self._collection = db.get_collection(name)

    def get(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int]) -> DatabaseEntryModel:
        return self.get_all(filter, partition_key)[0]

    def get_all(self, filter: Union[str, int, Dict[str, Union[int, float, str]]], partition_key: Union[str, int]) -> List[DatabaseEntryModel]:
        if isinstance(filter, (str, int)):
            filter = {self._ID_KEY: filter}
        elif isinstance(filter, dict):
            filter = dict(filter)
        else:
            raise TypeError('Unknown type')
        filter[self._PARTITION_KEY] = partition_key
        res = self._collection.find(filter)
        records = list(res)
        res.close()
        if len(records) == 0:
            raise RecordNotFound('No record found.')
        return self._parse_response(records)

    def insert(self, db_entry: DatabaseEntryModel) -> Union[str, int]:
        document = self._parse_document(db_entry)
        try:
            res = self._collection.insert_one(document)
        except DuplicateKeyError as e:
            self._logger.exception(e)
            raise RecordAlreadyExist('Record already exist')
        if not res.acknowledged:
            raise DatabaseOperationFailed('Something went wrong.')
        return res.inserted_id

    def insert_or_update(self, db_entry: DatabaseEntryModel) -> Union[str, int]:
        self._update(db_entry, upsert=True)

    def update(self, db_entry: DatabaseEntryModel):
        self._update(db_entry)

    def delete(self, id: Union[str, int], partition_key: Union[str, int]):
        res = self._collection.delete_one({self._ID_KEY: id, self._PARTITION_KEY: partition_key})
        if not res.acknowledged:
            raise DatabaseOperationFailed('Something went wrong.')
        if res.deleted_count == 0:
            raise RecordNotFound('Record do not exist or already deleted.')

    def _update(self, db_entry: DatabaseEntryModel, upsert = False):
        if db_entry.id is None:
            raise ValueError('DatabaseEntryModel.id can not be None')
        document = self._parse_document(db_entry)
        res = self._collection.update_one({self._ID_KEY: db_entry.id}, {'$set': document}, upsert=upsert)
        if res.matched_count == 0:
            raise RecordNotFound('Record not found.')
        if res.modified_count == 0:
            raise RecordUpdateFailed('Could not update record.')
        return res

    def _parse_document(self, db_entry: DatabaseEntryModel):
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
        return document

    def _parse_response(self, res: List[dict]) -> List[DatabaseEntryModel]:
        parsed_res = []
        for r in res:
            id = str(r.pop(self._ID_KEY))
            pkey = r.pop(self._PARTITION_KEY, None)
            etag = r.pop(self._ETAG_KEY, '*')
            e = DatabaseEntryModel(r, pkey, etag, id)
            parsed_res.append(e)
        return parsed_res
