from abc import abstractmethod
from jwt.jwk import AbstractJWKBase
from typing import List

class KeyHandler(object):

    @abstractmethod
    def get(self) -> List[AbstractJWKBase]:
        raise NotImplementedError()