from ._cosmos_client_builder import CosmosClientBuilderFromKeyvaultSecret
from ._cosmos_container_handler import CosmosContainerHandler

def create_database_container_if_not_exists(
    client_builder: CosmosClientBuilderFromKeyvaultSecret,
    database_name: str,
    containers: tuple,
    offer_throughput: str):
    from azure.cosmos.exceptions import CosmosHttpResponseError
    from azure.cosmos import CosmosClient, PartitionKey
    from http import HTTPStatus
    from common import exceptions

    client_list = client_builder.get_clients()
    retries = len(client_list)

    for client in client_list:
        try:
            client.create_database_if_not_exists(database_name, offer_throughput=offer_throughput)
            for container_name in containers:
                db_client = client.get_database_client(database_name)
                db_client.create_container_if_not_exists(container_name, PartitionKey(path='/partition_key'))
        except CosmosHttpResponseError as e:
                if retries > 1 and e.status_code == HTTPStatus.UNAUTHORIZED:
                    retries -= 1
                    continue
                raise exceptions.Unauthorized(e)
        break

from datetime import timedelta as _timedelta
def create_cosmos_container_handler(
    database_name: str,
    container_name: str,
    cache_timeout: _timedelta,
    client_builder: CosmosClientBuilderFromKeyvaultSecret):
    cosmos_container_handler = CosmosContainerHandler(database_name, container_name, client_builder, cache_timeout)
    return cosmos_container_handler