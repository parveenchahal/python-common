from datetime import timedelta

class Cache(object):

    _default_ttl: timedelta
    _namespace: str

    def __init__(self, namespace: str, default_ttl: timedelta = timedelta(days=1)) -> None:
        self._namespace = namespace
        self._default_ttl = default_ttl

    def get(self, key: str):
        raise NotImplementedError()

    def set(self, key: str, value: str):
        raise NotImplementedError()

    def _get_key(self, key):
        namespace = self._namespace
        return f'{key}-{namespace}'
