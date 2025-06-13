import pytest

from backend_service.dependencies.client_session_dependencies import (
    get_admin_session,
    get_client_session,
)
from backend_service.exceptions.controller_exceptions import (
    ForbiddenException,
    UnauthorizedException,
    UserNotFoundException,
)
from backend_service.services.auth_service import generate_auth_token

pytestmark = pytest.mark.anyio
MIN_USER_ID = 1
BEARER_TOKEN_PREFIX = 'Bearer '


async def test_get_client_session(create_tables, access_token, orm_session):
    assert await get_client_session(
        access_token.replace(BEARER_TOKEN_PREFIX, ''), orm_session
    )


async def test_fail_get_client_session_invalid_token(
    create_tables, access_token, orm_session
):
    with pytest.raises(UnauthorizedException):
        assert await get_client_session(access_token, orm_session)


async def test_fail_get_client_session_no_user(
    create_tables, orm_session, faker
):
    token = generate_auth_token(faker.pyint(min_value=MIN_USER_ID))
    with pytest.raises(UserNotFoundException):
        assert await get_client_session(token, orm_session)


async def test_fail_get_client_session_user_deactivated(
    create_tables, access_token, orm_session, logged_user
):
    logged_user.deactivate()
    orm_session.add(logged_user)
    orm_session.commit()

    with pytest.raises(UnauthorizedException):
        assert await get_client_session(access_token, orm_session)


async def test_get_admin_session(
    create_tables, access_token, orm_session, logged_user
):
    logged_user.is_admin = True

    assert await get_admin_session(logged_user)


async def test_fail_get_admin_session(
    create_tables, access_token, orm_session, logged_user
):
    logged_user.is_admin = False

    with pytest.raises(ForbiddenException):
        assert await get_admin_session(logged_user)
