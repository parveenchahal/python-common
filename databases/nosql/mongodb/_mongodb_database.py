from logging import Logger
from pymongo import MongoClient

class MongoDBDatabase:

    _logger: Logger

    def __init__(self, logger: Logger, name: str, client: MongoClient) -> None:
        self._logger = logger
        self._db = client[name]

    def get_collection(self, name: str):
        return self._db[name]
