class CosmosConnectionStringParser(object):

    _url: str
    _primary_key: str
    _secondary_key: str

    def __init__(self, primary_connection_string: str, secondary_connection_string: str = None):
        p = CosmosConnectionStringParser._convert_to_dict(primary_connection_string)
        s = None
        if secondary_connection_string is not None:
            s = CosmosConnectionStringParser._convert_to_dict(secondary_connection_string)
        try:
            self._url = p['AccountEndpoint']
        except:
            raise ValueError('AccountEndpoint not found in primary_connection_string')
        try:
            self._primary_key = p['AccountKey']
            if s is not None:
                self._secondary_key = s['AccountKey']
            else:
                self._secondary_key = None
        except:
            raise ValueError('AccountKey not found in atleast one of the connection_string')

    @staticmethod
    def _convert_to_dict(connection_string: str) -> dict:
        d = {}
        for param in connection_string.split(';'):
            k, v = param.split('=', 1)
            d[k] = v
        return d

    @property
    def url(self) -> str:
        return self._url

    @property
    def primary_key(self) -> str:
        return self._primary_key

    @property
    def secondary_key(self) -> str:
        return self._secondary_key
