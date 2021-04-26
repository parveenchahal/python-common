from datetime import timedelta

class CacheDecorator(object):
    def cache(self, ttl: timedelta = None, limit: int = None, namespace: str = None):
        raise NotImplementedError()