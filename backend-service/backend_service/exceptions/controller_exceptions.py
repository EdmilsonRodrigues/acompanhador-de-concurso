from fastapi import HTTPException


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
