from ._certificate_handler import CertificateHandler
from requests import get as http_get, request
from datetime import datetime, timedelta
from typing import List
import copy
from threading import RLock
from .models._certificate import Certificate
from common.utils import parse_json, to_json_string
from common.key_vault import KeyVaultSecret

class CertificateFromKeyvault(CertificateHandler):

    _key_vault_secret: KeyVaultSecret
    _cached_secret: List[Certificate]
    _next_read: datetime
    _cache_timeout: timedelta
    _lock: RLock

    def __init__(self, key_vault_secret: KeyVaultSecret, cache_timeout: timedelta):
        self._key_vault_secret = key_vault_secret
        self._cached_secret = None
        self._cache_timeout = cache_timeout
        self._next_read = None
        self._lock = RLock()

    def _update_required(self, now):
        return self._cached_secret is None or self._next_read is None or now >= self._next_read

    def get(self) -> List[Certificate]:
        now = datetime.utcnow()
        if self._update_required(now):
            with self._lock:
                if self._update_required(now):
                    secret = self._key_vault_secret.get()
                    cert_list = parse_json(secret)
                    cert_list = [Certificate.from_json_string(Certificate, to_json_string(x)) for x in cert_list]
                    self._cached_secret = cert_list
                    self._next_read = now + self._cache_timeout
        return copy.deepcopy(self._cached_secret)