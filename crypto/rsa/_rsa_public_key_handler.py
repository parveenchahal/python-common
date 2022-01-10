from typing import List
from jwt.jwk import AbstractJWKBase, RSAJWK, default_backend, jwk_from_pem
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from .._certificate_handler import CertificateHandler
from ._key_handler import KeyHandler


class RSAPublicKeyHandler(KeyHandler):
    _certificate_handler: CertificateHandler

    def __init__(self, certificate_handler: CertificateHandler):
        self._certificate_handler = certificate_handler

    def _get_key_obj(self, key: bytes) -> RSAJWK:
        cert = x509.load_pem_x509_certificate(key, default_backend())
        public_key = cert.public_key().public_bytes(Encoding.PEM, PublicFormat.PKCS1)
        public_key = jwk_from_pem(public_key)
        return public_key

    def get(self) -> List[AbstractJWKBase]:
        cert_list = self._certificate_handler.get()
        return [self._get_key_obj(cert.certificate) for cert in cert_list]

