class LoginFailureError(Exception):
    pass

class Unauthorized(Exception):
    pass

class MissingParamError(Exception):
    pass

class CannotBeCalledMoreThanOnceError(Exception):
    pass

class SessionTokenNotFoundError(Exception):
    pass

class SessionExpiredError(Exception):
    pass

class SessionRequiredRefreshError(Exception):
    pass

class JWTTokenInvalidSignatureError(Exception):
    pass

class ShouldNotHaveReachedHereError(Exception):
    pass

class EtagMismatchError(Exception):
    pass

class IncorrectValue(Exception):
    pass