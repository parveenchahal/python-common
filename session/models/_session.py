from dataclasses import dataclass
import copy
from datetime import datetime
from ... import Model
from dataclasses import dataclass


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
        d = super().to_dict(True)
        return d

    @property
    def is_expired(self) -> bool:
        now = int(datetime.timestamp(datetime.utcnow()))
        return now >= self.exp

    @property
    def refresh_required(self):
        now = int(datetime.timestamp(datetime.utcnow()))
        return now >= self.raf