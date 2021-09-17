from datetime import timedelta

class CacheDecorator(object):
    def cache(self, ttl: timedelta = None, namespace: str = None):
        raise NotImplementedError()