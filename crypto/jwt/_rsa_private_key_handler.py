from datetime import datetime, timedelta
from threading import RLock
from jwt.jwk import AbstractJWKBase, RSAJWK, load_pem_private_key, default_backend
from .._certificate_handler import CertificateHandler
from ._key_handler import KeyHandler
from typing import List

class Caching(object):
    def __init__(self):
        pass

class RSAPrivateKeyHandler(KeyHandler):

    _lock: RLock
    _certificate_handler: CertificateHandler
    _key_list: List[AbstractJWKBase]
    _cache_timeout: timedelta
    _next_read: datetime

    def __init__(self, certificate_handler: CertificateHandler, cache_timeout: timedelta = timedelta(seconds=10)):
        self._certificate_handler = certificate_handler
        self._cache_timeout = cache_timeout
        self._lock = RLock()
        self._key_list = None
        self._next_read = None

    def _update_required(self, now):
        return self._key_list is None or self._next_read is None or now >= self._next_read

    def _get_key_obj(self, key: bytes) -> RSAJWK:
        key = load_pem_private_key(key, password=None, backend=default_backend())
        return RSAJWK(key)

    def get(self) -> List[AbstractJWKBase]:
        now = datetime.utcnow()
        if self._update_required(now):
            with self._lock:
                if self._update_required(now):
                    cert_list = self._certificate_handler.get()
                    self._key_list = [self._get_key_obj(cert.private_key) for cert in cert_list]
                    self._next_read = now + self._cache_timeout
        return self._key_list
