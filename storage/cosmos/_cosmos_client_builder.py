from threading import RLock
from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy
from common.key_vault import KeyVaultSecret
from common.utils import parse_json
from typing import Tuple

class CosmosClientBuilderFromKeyvaultSecret(object):

    _lock: RLock
    _key_vault_secret: KeyVaultSecret

    def __init__(self, key_vault_secret: KeyVaultSecret):
        self._lock = RLock()
        self._dict = {}
        self._key_vault_secret = key_vault_secret

    def get_clients(self) -> Tuple[CosmosClient]:
        secret = self._key_vault_secret.get()
        list_of_connection_string = parse_json(secret)
        p_client = CosmosClient.from_connection_string(list_of_connection_string[0])
        s_client = CosmosClient.from_connection_string(list_of_connection_string[1])
        return (p_client, s_client)
    
    def get_database_clients(self, database_name: str) -> Tuple[DatabaseProxy]:
        p_client, s_client = self.get_clients()
        return (p_client.get_database_client(database_name), s_client.get_database_client(database_name))

    def get_container_clients(self, database_name: str, container_name: str) -> Tuple[ContainerProxy]:
        p_client, s_client = self.get_database_clients(database_name)
        return (p_client.get_container_client(container_name), s_client.get_container_client(container_name))