from datetime import timedelta
from .._cache import Cache
from redis import Redis
from ...exceptions import KeyNotFoundInCacheError, SetCacheError

class RedisCache(Cache):

    _client: Redis

    def __init__(self, client: Redis, default_ttl: timedelta = timedelta(days=1), namespace: str = None) -> None:
        super().__init__(namespace, default_ttl)
        self._client = client

    def get(self, key: str):
        key = self._format_key(key)
        result = self._client.get(key)
        if result is not None:
            return result
        raise KeyNotFoundInCacheError()

    def set(self, key: str, value: str, ttl: timedelta = None):
        if ttl is None:
            ttl = self._default_ttl
        key = self._format_key(key)
        done = self._client.set(key, value, ex=ttl)
        if not done:
            raise SetCacheError()
