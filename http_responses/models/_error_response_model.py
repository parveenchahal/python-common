from dataclasses import dataclass
from ... import Model as _Model
from http import HTTPStatus

@dataclass
class ErrorResponseModel(_Model):
    http_status_code: HTTPStatus
    error_message: str
