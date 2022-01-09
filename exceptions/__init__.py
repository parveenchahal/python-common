class LoginFailureError(Exception): pass

class Unauthorized(Exception): pass

class MissingParamError(Exception): pass

class CannotBeCalledMoreThanOnceError(Exception): pass

class SessionTokenNotFoundError(Exception): pass

class SessionExpiredError(Exception): pass

class SessionRequiredRefreshError(Exception): pass

class JWTTokenInvalidSignatureError(Exception): pass

class ShouldNotHaveReachedHereError(Exception): pass

class EtagMismatchError(Exception): pass

class IncorrectValue(Exception): pass

class KeyvaultOperationFailed(Exception): pass

class KeyvaultSecretNotFoundError(Exception): pass

class KeyNotFoundInCacheError(Exception): pass

class SetCacheError(Exception): pass

class NotFoundError(Exception): pass