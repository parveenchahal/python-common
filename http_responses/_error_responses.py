from ._json_response import JSONResponse as _JSONResponse
import json
from http import HTTPStatus
from .models._error_response_model import ErrorResponseModel


class ErrorResponse(_JSONResponse):
    def __init__(self, error_message: str, status: HTTPStatus):
        err_res = ErrorResponseModel(**{
            "error_message": error_message,
            "http_status_code": status
        })
        
        super().__init__(err_res, status)

class BadRequestResponse(ErrorResponse):
    def __init__(self, error_message: str = "BadRequest"):
        super().__init__(error_message, HTTPStatus.BAD_REQUEST)


class NotFoundResponse(ErrorResponse):
    def __init__(self, error_message: str = "NotFound"):
        super().__init__(error_message, HTTPStatus.NOT_FOUND)

class UnauthorizedResponse(ErrorResponse):
    def __init__(self, error_message: str = "Unauthorized"):
        super().__init__(error_message, HTTPStatus.UNAUTHORIZED)

class InternalServerErrorResponse(ErrorResponse):
    def __init__(self, error_message: str = "InternalServerError"):
        super().__init__(error_message, HTTPStatus.INTERNAL_SERVER_ERROR)

