from .._cache_decorator import CacheDecorator
from redis_cache import CacheDecorator as RCD
from redis.client import Redis
from json import dumps, loads
from datetime import timedelta

class RedisCacheDecorator(CacheDecorator):

    def __init__(self, client: Redis, default_ttl: timedelta = timedelta(days=1)) -> None:
        self._client = client
        self._default_ttl = default_ttl

    def cache(self, ttl: timedelta = None, limit: int = None, namespace: str = None, serializer=dumps, deserializer=loads):
        if ttl is None:
            ttl = self._default_ttl
        return RCD(self._client, serializer=serializer, deserializer=deserializer, ttl=ttl.total_seconds(), limit=limit, namespace=namespace)
