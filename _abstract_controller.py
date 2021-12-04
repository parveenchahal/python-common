from logging import Logger
from flask_restful import Resource

class Controller(Resource):

    _logger: Logger
    endpoint: str

    def __init__(self, logger: Logger):
        self._logger = logger
        self.endpoint = self.endpoint

    def get(self):
        raise NotImplementedError('GET is not supported.')

    def post(self):
        raise NotImplementedError('POST is not supported.')

    def delete(self):
        raise NotImplementedError('DELETE is not supported.')