from dataclasses import dataclass
from common import Model as _Model

@dataclass
class SessionTokenResponse(_Model):
    session: str
