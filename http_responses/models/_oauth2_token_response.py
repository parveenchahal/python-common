from dataclasses import dataclass
from ... import Model as _Model

@dataclass
class Oath2TokenResponse(_Model):
    access_token: str
