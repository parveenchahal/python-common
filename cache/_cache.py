from datetime import timedelta

class Cache(object):

    _default_ttl: timedelta
    _namespace: str

    def __init__(self, namespace: str, default_ttl: timedelta = timedelta(days=1)) -> None:
        self._namespace = namespace
        self._default_ttl = default_ttl

    def get(self, key: str, deserializer = None):
        raise NotImplementedError()

    def set(self, key: str, value: object, ttl: timedelta = None, serializer = None):
        raise NotImplementedError()

    def delete(self, key: str):
        raise NotImplementedError()

    def _format_key(self, key):
        if self._namespace is not None:
            return f'{key}-{self._namespace}'
        return key
