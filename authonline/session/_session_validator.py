from ...crypto.jwt import JWTHandler
from .models import Session
from logging import Logger
from ... import exceptions

class SessionValidator(object):

    _logger: Logger
    _jwt_handler: JWTHandler

    def __init__(self, logger: Logger, jwt_handler: JWTHandler):
        self._logger = logger
        self._jwt_handler = jwt_handler
    
    def validate(self, session_token: str, validation_callback = None, ignore_refresh_expiry: bool = False):
        payload = self._jwt_handler.decode(session_token)
        session = Session(**payload)
        if session.is_expired:
            raise exceptions.SessionExpiredError()
        if not ignore_refresh_expiry and session.refresh_required:
            raise exceptions.SessionRequiredRefreshError()
        if validation_callback is not None:
            validation_callback(session)
