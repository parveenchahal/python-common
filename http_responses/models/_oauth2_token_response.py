from dataclasses import dataclass
from common import Model as _Model

@dataclass
class Oath2TokenResponse(_Model):
    access_token: str
