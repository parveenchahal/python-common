import copy
from .utils import json_to_obj as _json_to_obj, to_json_string as _to_json_string, dict_to_obj as _dict_to_obj
from typing import Any
from dataclasses import dataclass

@dataclass
class Model(object):

    def to_dict(self, omit_none: bool = False) -> dict:
        d = copy.deepcopy(self.__dict__)
        if omit_none:
            d = {k: v for k, v in d.items() if v is not None}
        return d

    def to_json_string(self, omit_none: bool = False) -> str:
        return _to_json_string(self.to_dict(omit_none))

    @staticmethod
    def from_json_string(cls, json_data: str) -> Any:
        return _json_to_obj(cls, json_data)

    @staticmethod
    def from_dict(cls, d: dict) -> Any:
        return _dict_to_obj(cls, d)