from requests import get as _http_get
from .utils import parse_json
from requests.exceptions import ConnectionError as _ConnectionError


class AADToken(object):

    _auth_urls: str = [
        'https://aadtoken.authonline.net?tenant={0}&client_id={1}&secret={2}&resource={3}'
    ]

    def __init__(self, client_id: str, secret: str, resource: str, tenant: str = 'common'):
        for i in range(len(self._auth_urls)):
            self._auth_urls[i] = self._auth_urls[i].format(tenant, client_id, secret, resource)
    
    @property
    def access_token(self):
        n = len(self._auth_urls)
        for i in range(n):
            try:
                res = _http_get(self._auth_urls[i])
                return parse_json(res.text)["access_token"]
            except _ConnectionError:
                if i < n - 1:
                    continue
                raise _ConnectionError('Not able to connect to auth endpoints to get AAD token.')
