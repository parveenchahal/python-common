from datetime import timedelta
import json
from redis import Redis
from .._cache import Cache
from ...exceptions import KeyNotFoundInCacheError, SetCacheError

class RedisCache(Cache):

    _client: Redis

    def __init__(
        self,
        client: Redis,
        default_ttl: timedelta = timedelta(days=1),
        namespace: str = None) -> None:
        super().__init__(namespace, default_ttl)
        self._client = client

    def get(self, key: str, deserializer = None):
        key = self._format_key(key)
        result = self._client.get(key)
        if result is None:
            raise KeyNotFoundInCacheError()
        result = json.loads(result)['v']
        if deserializer is not None:
            return deserializer(result)
        return result

    def set(self, key: str, value: object, ttl: timedelta = None, serializer = None):
        if ttl is None:
            ttl = self._default_ttl
        key = self._format_key(key)
        if serializer is not None:
            value = serializer(value)
        typ = type(value)
        if typ not in [str, int, float]:
            raise TypeError(f'Object type {typ} can\'t be cached. Supported types are (str, int, float)')
        done = self._client.set(key, json.dumps({'v': value}), ex=ttl)
        if not done:
            raise SetCacheError()

    def delete(self, key: str) -> bool:
        key = self._format_key(key)
        return self._client.delete(key) == 1