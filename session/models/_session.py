from dataclasses import dataclass
from datetime import datetime
from ... import Model

@dataclass
class Session(Model):
    sid: str
    amr: list
    oid: str
    app: str
    usr: str
    res: str
    exp: int
    raf: int
    sqn: int
    
    def to_dict(self) -> dict:
        return super().to_dict(True)

    @property
    def is_expired(self) -> bool:
        now = int(datetime.timestamp(datetime.utcnow()))
        return now >= self.exp

    @property
    def refresh_required(self):
        now = int(datetime.timestamp(datetime.utcnow()))
        return now >= self.raf
