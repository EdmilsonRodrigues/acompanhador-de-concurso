from typing import Annotated

from fastapi import Depends

from ..exceptions.controller_exceptions import (
    ForbiddenException,
    UnauthorizedException,
    UserNotFoundException,
)
from ..exceptions.services_exceptions import InvalidTokenException
from ..models.user_model import User
from ..services.auth_service import AuthToken, decode_jwt_token
from .services_dependencies import ORMSessionDependency


async def get_client_session(
    auth_token: AuthToken, orm_session: ORMSessionDependency
) -> User:
    try:
        user_id = decode_jwt_token(auth_token)
    except InvalidTokenException as exc:
        raise UnauthorizedException from exc

    user = orm_session.get(User, user_id)
    if user is None or not user.is_active:
        raise UserNotFoundException

    return user


ClientSessionDependency = Annotated[User, Depends(get_client_session)]


async def get_admin_session(user: ClientSessionDependency):
    if not user.is_admin:
        raise ForbiddenException

    return user


AdminSessionDependency = Annotated[User, Depends(get_admin_session)]
