from datetime import timedelta
from ._cache import Cache
from ..exceptions import KeyNotFoundInCacheError
import json

class CacheDecorator(object):
    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def cache(self, ttl: timedelta = None, serializer=None, deserializer=None):
        def wrapper(f):
            def inner(*args, **kwargs):
                try:
                    key = '-'.join(map(str, args)) + '-'.join([(str(k), str(v)) for k,v in kwargs.items()])
                    res = self._cache.get(key)
                    if deserializer is not None:
                        res = deserializer(res)
                    res = json.loads(res)
                    return res['v']
                except KeyNotFoundInCacheError:
                    res = f(*args, **kwargs)
                    if serializer is not None:
                        res = serializer(res)
                    if ttl is None:
                        self._cache.set(key, json.dumps({'v': res}))
                    else:
                        self._cache.set(key, json.dumps({'v': res}), ttl=ttl)
                    return res
            return inner
        return wrapper
