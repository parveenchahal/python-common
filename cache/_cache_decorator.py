from datetime import timedelta
from ._cache import Cache
from ..exceptions import KeyNotFoundInCacheError

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
        res = cache.get(key, deserializer)
        return res
    except KeyNotFoundInCacheError:
        if class_instance is None:
            res = f(*args, **kwargs)
        else:
            res = f(class_instance, *args, **kwargs)
        cache.set(key, res, ttl, serializer)
        return res
    except Exception:
        if class_instance is None:
            res = f(*args, **kwargs)
        else:
            res = f(class_instance, *args, **kwargs)
        return res
