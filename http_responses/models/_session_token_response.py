from dataclasses import dataclass
from ... import Model as _Model

@dataclass
class SessionTokenResponse(_Model):
    session: str
