class ServiceException(Exception):
    default_message: str

    def __init__(self, *args):
        if not args:
            super().__init__(self.default_message)
        else:
            super().__init__(*args)


class InvalidTokenException(ServiceException):
    default_message = 'Invalid token'


class UnmatchedPasswordException(ServiceException):
    default_message = 'Unmatched password'
