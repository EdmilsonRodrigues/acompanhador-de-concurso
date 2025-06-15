from fastapi import HTTPException, status


class ControllerException(HTTPException):
    status_code: int
    detail: str
    headers: dict = {}

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class WrongCredentialsException(ControllerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid username or password'


class InvalidDataException(ControllerException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__()


class UserWithEmailAlreadyExistsException(ControllerException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with email already exists'


class InvalidRefreshTokenException(ControllerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid refresh token'


class UnauthorizedException(ControllerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token'
    headers = {'WWW-Authenticate': 'Bearer'}


class ForbiddenException(ControllerException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User does not have permission to perform this action'


class UserNotFoundException(ControllerException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'


class SubscriptionNotFoundException(ControllerException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Subscription not found'


class SearchAlertNotFoundException(ControllerException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Search alert not found'
