from dataclasses import dataclass
from common import Model as _Model
from http import HTTPStatus

@dataclass
class MessageResponseModel(_Model):
    message: str

