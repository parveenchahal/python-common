from typing import List
from http import HTTPStatus
import json
from requests import get as http_get
from common.utils import string_to_bytes, decode_base64
from ..constants import AUTH_ONLINE_PUBLIC_CERTIFICATE
from ..cache import Cache, cached
from ._certificate_handler import CertificateHandler
from .models._certificate import Certificate
from ..exceptions import HTTPCallFailedError

class AuthonlinePublicCertificatesHandler(CertificateHandler):

    _cache: Cache
    _url: str

    def __init__(self, url: str = AUTH_ONLINE_PUBLIC_CERTIFICATE, cache: Cache = None) -> None:
        self._cache = cache
        self._url = url

    def get(self) -> List[Certificate]:
        if self._cache is not None:
            certs = self._get_cached()
        certs =  self._get()
        certs = json.loads(certs)
        return [Certificate(string_to_bytes(decode_base64(cert))) for cert in certs]

    def _get(self):
        res = http_get(self._url)
        if res.status_code != HTTPStatus.OK:
            return res.text
        raise HTTPCallFailedError(f'Getting cert from authonline failed with status code {res.status_code}.')

    def _get_cached(self):
        @cached(self._cache)
        def wrapper():
            return self._get()
        return wrapper()