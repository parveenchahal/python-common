from datetime import timedelta
from ._cache import Cache
from ..exceptions import KeyNotFoundInCacheError
import json

class CacheDecorator(object):
    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def __cache(self, f, class_instance, ttl, serializer, deserializer, *args, **kwargs):
        try:
            key = '-'.join(map(str, args)) + '-'.join([(str(k), str(v)) for k,v in kwargs.items()])
            res = self._cache.get(key)
            if deserializer is not None:
                res = deserializer(res)
            res = json.loads(res)
            return res['v']
        except KeyNotFoundInCacheError:
            if class_instance is None:
                res = f(*args, **kwargs)
            else:
                res = f(class_instance, *args, **kwargs)
            if serializer is not None:
                res = serializer(res)
            if ttl is None:
                self._cache.set(key, json.dumps({'v': res}))
            else:
                self._cache.set(key, json.dumps({'v': res}), ttl=ttl)
            return res

    def cache(self, ttl: timedelta = None, serializer=None, deserializer=None):
        def wrapper(f):
            def inner(*args, **kwargs):
                self.__cache(f, None, ttl, serializer, deserializer, *args, **kwargs)
            return inner
        return wrapper

    def cache_method(self, ttl: timedelta = None, serializer=None, deserializer=None):
        def wrapper(f):
            def inner(class_instance, *args, **kwargs):
                self.__cache(f, class_instance, ttl, serializer, deserializer, *args, **kwargs)
            return inner
        return wrapper
