from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from sqlmodel import select

from ..dependencies.services_dependencies import ORMSessionDependency
from ..exceptions.controller_exceptions import (
    InvalidRefreshTokenException,
    UserWithEmailAlreadyExistsException,
    WrongCredentialsException,
)
from ..exceptions.services_exceptions import (
    InvalidTokenException,
    UnmatchedPasswordException,
)
from ..models.user_model import User, UserCreate
from ..services.auth_service import (
    LoginForm,
    TokenData,
    check_password,
    decode_jwt_token,
    generate_auth_token,
    generate_refresh_token,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/signin', status_code=201)
async def signin(user: UserCreate, orm_session: ORMSessionDependency):
    db_user = User.model_validate(user)
    try:
        orm_session.add(db_user)
        orm_session.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise UserWithEmailAlreadyExistsException from exc

    return {'success': True}


@router.post('/login', status_code=200, response_model=TokenData)
async def login(form_data: LoginForm, orm_session: ORMSessionDependency):
    statement = select(User).where(User.email == form_data.username)
    user = orm_session.exec(statement).one_or_none()
    if user is None or user.id is None:
        raise WrongCredentialsException

    try:
        check_password(form_data.password, user.password)
    except UnmatchedPasswordException as exc:
        raise WrongCredentialsException from exc

    refresh_token = generate_refresh_token(user.id)
    response = JSONResponse(
        content={
            'access_token': generate_auth_token(user.id),
            'token_type': 'bearer',
        }
    )

    response.set_cookie(
        key='refresh_token', value=refresh_token, httponly=True
    )

    return response


@router.post('/refresh', status_code=200, response_model=TokenData)
async def refresh_session(
    refresh_token: Annotated[str, Cookie()],
    orm_session: ORMSessionDependency,
):
    try:
        user_id = decode_jwt_token(refresh_token)
    except InvalidTokenException as exc:
        raise InvalidRefreshTokenException from exc

    return {
        'access_token': generate_auth_token(user_id),
        'token_type': 'bearer',
    }
