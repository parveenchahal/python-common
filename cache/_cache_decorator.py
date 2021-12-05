from datetime import timedelta
from ._cache import Cache
from ..exceptions import KeyNotFoundInCacheError
import json

def cached(cache: Cache, ttl: timedelta = None, serializer=None, deserializer=None):
    def wrapper(f):
        def inner(*args, **kwargs):
            return __cache(cache, f, None, ttl, serializer, deserializer, *args, **kwargs)
        return inner
    return wrapper

def cached_method(cache: Cache, ttl: timedelta = None, serializer=None, deserializer=None):
    def wrapper(f):
        def inner(class_instance, *args, **kwargs):
            return __cache(
                cache, f, class_instance, ttl, serializer, deserializer, *args, **kwargs)
        return inner
    return wrapper

def __cache(cache: Cache, f, class_instance, ttl, serializer, deserializer, *args, **kwargs):
    try:
        key = '-'.join(map(str, args)) + '-'.join([(str(k), str(v)) for k,v in kwargs.items()])
        res = cache.get(key)
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
        typ = type(serialized_res)
        if typ not in [str, int, float]:
            raise TypeError(f'Object type {typ} can\'t be cached. Supported types are (str, int, float)')
        if ttl is None:
            cache.set(key, json.dumps({'v': serialized_res}))
        else:
            cache.set(key, json.dumps({'v': serialized_res}), ttl=ttl)
        return res
    except Exception:
        if class_instance is None:
            res = f(*args, **kwargs)
        else:
            res = f(class_instance, *args, **kwargs)
        return res
