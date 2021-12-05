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
            res = json.loads(res)
            res = res['v']
            if deserializer is not None:
                res = deserializer(res)
            return res
        except KeyNotFoundInCacheError:
            if class_instance is None:
                res = f(*args, **kwargs)
            else:
                res = f(class_instance, *args, **kwargs)

            serialized_res = res
            if serializer is not None:
                serialized_res = serializer(res)

            if ttl is None:
                self._cache.set(key, json.dumps({'v': serialized_res}))
            else:
                self._cache.set(key, json.dumps({'v': serialized_res}), ttl=ttl)
            return res
        except Exception:
            if class_instance is None:
                res = f(*args, **kwargs)
            else:
                res = f(class_instance, *args, **kwargs)
            return res

    def cached(self, ttl: timedelta = None, serializer=None, deserializer=None):
        def wrapper(f):
            def inner(*args, **kwargs):
                return self.__cache(f, None, ttl, serializer, deserializer, *args, **kwargs)
            return inner
        return wrapper

    def cached_method(self, ttl: timedelta = None, serializer=None, deserializer=None):
        def wrapper(f):
            def inner(class_instance, *args, **kwargs):
                return self.__cache(
                    f, class_instance, ttl, serializer, deserializer, *args, **kwargs)
            return inner
        return wrapper
