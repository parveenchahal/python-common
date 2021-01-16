from datetime import datetime
from ..crypto.jwt import JWTHandler
from ..session.models import Session
from logging import Logger
import functools
from flask import request
from .. import exceptions
from .. import http_responses

class _SessionValidator(object):

    _logger: Logger
    _jwt_handler: JWTHandler

    def __init__(self, logger: Logger, jwt_handler: JWTHandler):
        self._logger = logger
        self._jwt_handler = jwt_handler
    
    def _validate(self, session_token: str, ignore_refresh_expiry: bool):
        payload = self._jwt_handler.decode(session_token)
        session = Session(**payload)
        if session.is_expired:
            raise exceptions.SessionExpiredError()
        if not ignore_refresh_expiry and session.refresh_required:
            raise exceptions.SessionRequiredRefreshError()

    def validate(self, session_token: str, ignore_refresh_expiry: bool = False):
        try:
            _session_validator._validate(session_token, ignore_refresh_expiry)
        except exceptions.SessionRequiredRefreshError as ex:
            self._logger.exception(ex)
            return http_responses.UnauthorizedResponse("Session required refresh.")
        except exceptions.SessionExpiredError as ex:
            self._logger.exception(ex)
            return http_responses.UnauthorizedResponse("Session expired.")
        except Exception as ex:
            self._logger.exception(ex)
            return http_responses.UnauthorizedResponse("Session token can't be validated")
        

_session_validator = None

def init_session_validator(logger: Logger, jwt_handler: JWTHandler):
    global _session_validator
    if _session_validator is None:
        _session_validator = _SessionValidator(logger, jwt_handler)
    else:
        raise exceptions.CannotBeCalledMoreThanOnceError("init_session_validator can't be called more than once")

def _validate_session(f, ignore_refresh_expiry, *args, **kwargs):
    session_token: str = None
    try:
        session_token = request.headers['Authorization']
    except KeyError:
        return http_responses.UnauthorizedResponse("Session token not found in request.")
    if not session_token.startswith('Bearer'):
        return http_responses.UnauthorizedResponse("Bearer scheme is missing in Authorization header.")
    session_token = session_token.split(' ', 1)[1]
    res = _session_validator.validate(session_token, ignore_refresh_expiry)
    if res is None:
        return f(*args, **kwargs)
    return res

def validate_session(f=None, ignore_refresh_expiry=False):
    is_callable = callable(f)
    if is_callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return _validate_session(f, ignore_refresh_expiry, *args, **kwargs)
        return wrapper
    else:
        def inner(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return _validate_session(f, ignore_refresh_expiry, *args, **kwargs)
            return wrapper
        return inner
