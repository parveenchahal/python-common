from logging import Logger
from datetime import datetime, timedelta
import pytz
import functools
from flask import request, redirect
from ...crypto.rsa import RSAPublicKeyHandler
from ...crypto.jwt import JWTHandler
from ...crypto import CertificateHandler
from ._authonline_session_handler import AuthOnlineSessionHandler
from ._session_validator import SessionValidator
from ... import exceptions, http_responses
from ...crypto.jwt import JWTHandler

_logger: Logger = None
_login_uri: str = None
_auth_online_session_handler: AuthOnlineSessionHandler = None
_session_validator: SessionValidator = None

def init_cookie_handler_for_flask(
    logger: Logger,
    authonline_cert_handler: CertificateHandler,
    login_uri):
    global _logger, _auth_online_session_handler, _login_uri, _session_validator
    _logger = logger
    _login_uri = login_uri
    _auth_online_session_handler = AuthOnlineSessionHandler(logger)
    rsa_public_key_handler = RSAPublicKeyHandler(authonline_cert_handler)
    jwt_handler = JWTHandler(rsa_public_key_handler, rsa_public_key_handler)
    _session_validator = SessionValidator(logger, jwt_handler)

def validate_cookie_session(f=None, validation_callback = None, ignore_refresh_expiry=False):
    is_callable = callable(f)
    if is_callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return _validate_cookie_session(f, validation_callback, ignore_refresh_expiry, *args, **kwargs)
        return wrapper
    else:
        def inner(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return _validate_cookie_session(f, validation_callback, ignore_refresh_expiry, *args, **kwargs)
            return wrapper
        return inner

def _validate_cookie_session(f, validation_callback, ignore_refresh_expiry, *args, **kwargs):
    path = request.path
    login_url = _login_uri.format(PATH=path)
    session: str = request.cookies.get('session', None)
    if session is None:
        return redirect(login_url)
    refreshed_session = None
    try:
        _session_validator.validate(session, validation_callback, ignore_refresh_expiry)
        _, session_payload, _ = session.split(".")
        raf = int(JWTHandler.decode_payload(session_payload)["raf"])
        if (datetime.fromtimestamp(raf) - timedelta(minutes=1)) <= datetime.utcnow():
            raise exceptions.SessionRequiredRefreshError('Refreshing 1 minute prior to actual refresh time')
    except exceptions.Unauthorized as e:
        _logger.exception(e)
        return redirect(login_url)
    except exceptions.SessionRequiredRefreshError:
        try:
            # TODO: Need to add retry
            refreshed_session = _auth_online_session_handler.refresh(session)
        except exceptions.SessionRefreshFailed as e:
            _logger.exception(e)
            return http_responses.InternalServerErrorResponse()
        except exceptions.Unauthorized as e:
            _logger.exception(e)
            return redirect(login_url)
    except Exception as e:
        _logger.exception(e)
        return http_responses.InternalServerErrorResponse()
    res = f(*args, **kwargs)
    if refreshed_session is not None:
        _, session_payload, _ = refreshed_session.split(".")
        expiry = int(JWTHandler.decode_payload(session_payload)["exp"])
        expiry = datetime.fromtimestamp(expiry, pytz.utc)
        res.set_cookie('session', refreshed_session, expires=expiry, secure=True, httponly=True)
    return res
    
