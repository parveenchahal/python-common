from flask_restful import Resource, ResponseBase as _Response
from logging import Logger
from .utils import to_json_string


class Controller(Resource):

    _logger: Logger
    endpoint: str

    def __init__(self, logger: Logger):
        self._logger = logger
        self.endpoint = self.endpoint

    def get(self):
        raise NotImplemented('GET is not supported.')

    def post(self):
        raise NotImplemented('POST is not supported.')

    def delete(self):
        raise NotImplemented('DELETE is not supported.')