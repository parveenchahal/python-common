from typing import List
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from jwt.jwk import AbstractJWKBase, RSAJWK, jwk_from_pem
from .._certificate_handler import CertificateHandler
from ._key_handler import KeyHandler


class RSAPrivateKeyHandler(KeyHandler):

    _certificate_handler: CertificateHandler

    def __init__(self, certificate_handler: CertificateHandler):
        self._certificate_handler = certificate_handler

    def get(self) -> List[AbstractJWKBase]:
        cert_list = self._certificate_handler.get()
        key_list = [jwk_from_pem(cert.private_key) for cert in cert_list]
        return key_list
