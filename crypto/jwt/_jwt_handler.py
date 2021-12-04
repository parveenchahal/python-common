from jwt import JWT
from ._key_handler import KeyHandler
from jwt.utils import b64decode as _b64decode
from ...utils import bytes_to_string, parse_json
from ... import exceptions

class JWTHandler(object):
    _jwt: JWT
    _signing_key_handler: KeyHandler
    _sig_verify_key_handler: KeyHandler
    _alg: str

    def __init__(
        self,
        signing_key_handler: KeyHandler,
        sig_verify_key_handler: KeyHandler,
        alg: str = "RS256"):
        self._signing_key_handler = signing_key_handler
        self._sig_verify_key_handler = sig_verify_key_handler
        self._alg = alg
        self._jwt = JWT()

    def encode(self, payload: dict) -> str:
        key = self._signing_key_handler.get()[0]
        jwt_token = self._jwt.encode(payload, key, alg=self._alg)
        return jwt_token

    def decode(self, token: str, verify_signature: bool = True) -> dict:
        if verify_signature:
            key_list = self._sig_verify_key_handler.get()
            if key_list is None or len(key_list) <= 0:
                raise ValueError("Can't decode, list of keys is None or empty list.")
            for key in key_list:
                exception_occured = None
                try:
                    payload = self._jwt.decode(
                        token, key, algorithms=self._alg, do_time_check=False)
                except Exception as ex:
                    exception_occured = ex
            if exception_occured is None:
                return payload
            raise exceptions.JWTTokenInvalidSignatureError("Invalid Signature")
        return JWTHandler.decode_payload(token.split('.')[1])

    @staticmethod
    def decode_payload(encoded_payload: str) -> dict:
        b = _b64decode(encoded_payload)
        return parse_json(bytes_to_string(b))