from jwt.jwk import AbstractJWKBase, RSAJWK, jwk_from_pem
from .._certificate_handler import CertificateHandler
from ._key_handler import KeyHandler
from typing import List

class Caching(object):
    def __init__(self):
        pass

class RSAPrivateKeyHandler(KeyHandler):

    _certificate_handler: CertificateHandler

    def __init__(self, certificate_handler: CertificateHandler):
        self._certificate_handler = certificate_handler

    def get(self) -> List[AbstractJWKBase]:
        cert_list = self._certificate_handler.get()
        key_list = [RSAJWK(jwk_from_pem(cert.private_key)) for cert in cert_list]
        return key_list
