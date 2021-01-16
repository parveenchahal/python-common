from abc import abstractmethod
from typing import List
from .models._certificate import Certificate

class CertificateHandler(object):
    
    @abstractmethod
    def get(self) -> List[Certificate]:
        raise NotImplementedError()