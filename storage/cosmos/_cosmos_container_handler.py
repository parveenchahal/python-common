from datetime import timedelta
from typing import List
from http import HTTPStatus
from cachetools import TTLCache, cached
from azure.core import MatchConditions
from azure.cosmos import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError, \
                                    CosmosAccessConditionFailedError, CosmosHttpResponseError
from ._cosmos_client_builder import CosmosClientBuilderFromKeyvaultSecret
from ...storage import Storage
from ...storage.models import StorageEntryModel
from ... import exceptions


class CosmosContainerHandler(Storage):

    _database_name: str
    _container_name: str
    _client_builder: CosmosClientBuilderFromKeyvaultSecret

    def __init__(
        self,
        database_name: str,
        container_name: str,
        client_builder: CosmosClientBuilderFromKeyvaultSecret,
        cache_timeout: timedelta):
        self._database_name = database_name
        self._container_name = container_name
        self._client_builder = client_builder
        self._ttl_cache = TTLCache(10, cache_timeout.total_seconds())

    def get(self, id: str, partition_key: str) -> StorageEntryModel:
        client_list = self._get_cached_or_create_clients()
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
                'data': data,
                'etag': data.get('_etag', '*')
            })
            return entry
        raise exceptions.ShouldNotHaveReachedHereError()
    
    def add_or_update(self, storage_entry: StorageEntryModel):
        body = storage_entry.data
        body['id'] = storage_entry.id
        body['partition_key'] = storage_entry.partition_key

        client_list = self._get_cached_or_create_clients()
        retries = len(client_list)
        for client in client_list:
            try:
                client.upsert_item(
                    body=body,
                    etag=storage_entry.etag,
                    match_condition=MatchConditions.IfNotModified)
            except CosmosAccessConditionFailedError:
                raise exceptions.EtagMismatchError()
            except CosmosHttpResponseError as e:
                if retries > 1 and e.status_code == HTTPStatus.UNAUTHORIZED:
                    retries -= 1
                    continue
                raise exceptions.Unauthorized(e)
            break

    def _get_cached_or_create_clients(self) -> List[ContainerProxy]:
        @cached(self._ttl_cache)
        def wrapper():
            return self._client_builder.get_container_clients(self._database_name, self._container_name)
        return wrapper()
