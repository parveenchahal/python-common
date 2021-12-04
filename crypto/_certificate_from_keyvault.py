from typing import List
from ._certificate_handler import CertificateHandler
from .models._certificate import Certificate
from ..utils import parse_json, to_json_string
from ..key_vault import KeyVaultSecret
from ..cache import Cache, CacheDecorator

class CertificateFromKeyvault(CertificateHandler):

    _key_vault_secret: KeyVaultSecret
    _cache: CacheDecorator

    def __init__(self, key_vault_secret: KeyVaultSecret, cache: Cache = None):
        self._key_vault_secret = key_vault_secret
        if cache is not None:
            self._cache = CacheDecorator(cache)

    def _get(self):
        if self._cache is not None:
            @self._cache.cached()
            def wrapper():
                return self._key_vault_secret.get()
            return wrapper()
        return self._key_vault_secret.get()

    def get(self) -> List[Certificate]:
        secret = self._get()
        cert_list = parse_json(secret)
        return [Certificate.from_json_string(Certificate, to_json_string(x)) for x in cert_list]