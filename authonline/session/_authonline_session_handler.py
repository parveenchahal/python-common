from logging import Logger, exception
import json
from http import HTTPStatus
from requests import get as http_get

from common import exceptions


class AuthOnlineSessionHandler(object):

    _logger: Logger
    REFRESH_SESSION_URL = 'https://apis.authonline.net/session/refresh'
    LOGOUT_SESSION_URL = 'https://apis.authonline.net/session/logout'

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def refresh(self, session: str) -> str:
        res = http_get(self.REFRESH_SESSION_URL, headers={'Session': session})
        if res.status_code == HTTPStatus.OK:
            return json.loads(res.text)['session']
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            raise exceptions.Unauthorized()
        raise exceptions.SessionRefreshFailed()

    def logout(self, session: str):
        res = http_get(self.LOGOUT_SESSION_URL, headers={'Session': session})
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            raise exceptions.Unauthorized()
        if res.status_code != HTTPStatus.OK:
            raise exceptions.SessionRefreshFailed()
        
