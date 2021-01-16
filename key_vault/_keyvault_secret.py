from requests import request
from common.utils import parse_json
from common import AADToken

class KeyVaultSecret(object):

    _secret_url: str = 'https://{0}.vault.azure.net/secrets/{1}?api-version={2}'
    _aad_token: AADToken

    def __init__(self, keyvault_name: str, secret_name: str, aad_token: AADToken, api_version: str = '2016-10-01'):
        self._secret_url = self._secret_url.format(keyvault_name, secret_name, api_version)
        self._aad_token = aad_token

    def get(self) -> str:
        access_token = self._aad_token.access_token
        res = request("GET", self._secret_url, headers={"Authorization": f'Bearer {access_token}'})
        value = parse_json(res.text)['value']
        return value