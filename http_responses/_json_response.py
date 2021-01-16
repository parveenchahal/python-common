from ._abstract_response import Response
from typing import Union, List, Text, Mapping, Sequence, Optional
from http import HTTPStatus
import json
from .. import Model

class JSONResponse(Response):

    def __init__(self,
        response: Union[Model, List[Model]],
        status: HTTPStatus = HTTPStatus.OK,
        headers: Optional[Sequence[Mapping[Text, Text]]] = None):
        if isinstance(response, List):
            response = JSONResponse.__convert_to_list_of_dict(response)
        else:
            response = response.to_dict()
        super().__init__(json.dumps(response), status.value, headers, "application/json")
    
    @staticmethod
    def __convert_to_list_of_dict(response_list: List[Model]):
        return [res.to_dict() for res in response_list]
