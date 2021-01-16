from dataclasses import dataclass
from ... import Model as _Model
from http import HTTPStatus

@dataclass
class MessageResponseModel(_Model):
    message: str

