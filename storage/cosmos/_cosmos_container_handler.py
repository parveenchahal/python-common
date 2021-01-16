from datetime import datetime, timedelta
from threading import RLock
from ._cosmos_client_builder import CosmosClientBuilderFromKeyvaultSecret
from azure.cosmos import ContainerProxy
from typing import List, Tuple
from common.storage import Storage
from common.storage.models import StorageEntryModel
from common import Model
from common import exceptions
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosAccessConditionFailedError, CosmosHttpResponseError
from azure.core import MatchConditions
from http import HTTPStatus


class CosmosContainerHandler(Storage):

    _database_name: str
    _container_name: str
    _client_builder: CosmosClientBuilderFromKeyvaultSecret
    _next_read: datetime = None
    _cache_timeout: timedelta
    _cached_container_clients: Tuple[ContainerProxy]
    _lock: RLock

    def __init__(self, database_name: str, container_name: str, client_builder: CosmosClientBuilderFromKeyvaultSecret, cache_timeout: timedelta):
        self._database_name = database_name
        self._container_name = container_name
        self._client_builder = client_builder
        self._cache_timeout = cache_timeout
        self._lock = RLock()

    def get(self, id: str, partition_key: str, model_for_data: Model) -> StorageEntryModel:
        client_list = self._get_clients()
        retries = len(client_list)
        for client in client_list:
            try:
                data = client.read_item(item=id, partition_key=partition_key)
            except CosmosResourceNotFoundError:
                return None
            except CosmosHttpResponseError as e:
                if retries > 1 and e.status_code == HTTPStatus.UNAUTHORIZED:
                    retries -= 1
                    continue
                raise exceptions.Unauthorized(e)

            entry = StorageEntryModel(**{
                'id': data['id'],
                'partition_key': data['partition_key'],
                'data': model_for_data.from_dict(model_for_data, data),
                'etag': data.get('_etag', '*')
            })
            return entry
        raise exceptions.ShouldNotHaveReachedHereError()
    
    def add_or_update(self, storage_entry: StorageEntryModel):
        body = storage_entry.data.to_dict()
        body['id'] = storage_entry.id
        body['partition_key'] = storage_entry.partition_key

        client_list = self._get_clients()
        retries = len(client_list)
        for client in client_list:
            try:
                client.upsert_item(body=body, etag=storage_entry.etag, match_condition=MatchConditions.IfNotModified)
            except CosmosAccessConditionFailedError:
                raise exceptions.EtagMismatchError()
            except CosmosHttpResponseError as e:
                if retries > 1 and e.status_code == HTTPStatus.UNAUTHORIZED:
                    retries -= 1
                    continue
                raise exceptions.Unauthorized(e)
            break

    def _update_required(self, now):
        return self._next_read is None or now >= self._next_read

    def _get_clients(self) -> List[ContainerProxy]:
        now = datetime.utcnow()
        if self._update_required(now):
            with self._lock:
                if self._update_required(now):
                    self._cached_container_clients = self._client_builder.get_container_clients(self._database_name, self._container_name)
                    self._next_read = now + self._cache_timeout
        return self._cached_container_clients

    