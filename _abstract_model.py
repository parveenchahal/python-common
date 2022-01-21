from ast import Mod
import copy
import json
from typing import Any, TypeVar
from dataclasses import dataclass
from .utils import json_to_obj as _json_to_obj, \
                    dict_to_obj as _dict_to_obj

T = TypeVar('T')

@dataclass
class Model(object):

    # It must to dict like {'user_id': 'userId'}
    __mapping__ = None

    def to_dict(self, omit_none: bool = False) -> dict:
        d = copy.deepcopy(self.__dict__)
        d.pop('__mapping__', None)
        if self.__mapping__ is not None:
            d = self._parse_dict_with_mapping(self.__mapping__, d)
        if omit_none:
            d = {k: v for k, v in d.items() if v is not None}
        return d

    def serialize(self, omit_none: bool = False) -> str:
        return json.dumps(self.to_dict(omit_none))

    @staticmethod
    def from_dict(cls: T, d: dict) -> T:
        if cls.__mapping__ is not None:
            rev_mapping = Model._reverse_mapping(cls.__mapping__)
            d = Model._parse_dict_with_mapping(rev_mapping, d)
        return _dict_to_obj(cls, d)

    @staticmethod
    def deserialize(cls: T, json_data: str) -> T:
        j = json.loads(json_data)
        return Model.from_dict(cls, j)

    @staticmethod
    def _parse_dict_with_mapping(mapping: dict, d: dict):
        return {mapping[k]: v for k,v in d.items()}

    @staticmethod
    def _reverse_mapping(mapping: dict):
        return {v: k for k,v in mapping.items()}