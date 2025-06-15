import pytest

from backend_service.models.user_model import UserCreate
from backend_service.services.auth_service import generate_refresh_token

pytestmark = pytest.mark.anyio


async def test_signin(async_client, user):
    payload = UserCreate(**user.model_dump()).model_dump()
    payload['password'] = user.password

    response = await async_client.post('/auth/signin', json=payload)
    assert response.status_code == 201


async def test_fail_signin_user_exist(async_client, logged_user):
    payload = UserCreate(**logged_user.model_dump()).model_dump()
    payload['password'] = logged_user.password

    response = await async_client.post('/auth/signin', json=payload)
    assert response.status_code == 409


async def test_login(async_client, logged_user):
    login_response = await async_client.post(
        '/auth/login',
        data={'username': logged_user.email, 'password': logged_user.password},
    )
    assert login_response.status_code == 200

    assert login_response.json()['token_type'] == 'bearer'
    assert login_response.cookies['refresh_token']


async def test_fail_login_wrong_password(async_client, logged_user, faker):
    login_response = await async_client.post(
        '/auth/login',
        data={'username': logged_user.email, 'password': faker.password()},
    )

    assert login_response.status_code == 401
    assert 'refresh_token' not in login_response.cookies


async def test_fail_login_user_not_exist(async_client, logged_user, faker):
    login_response = await async_client.post(
        '/auth/login',
        data={'username': faker.email(), 'password': logged_user.password},
    )

    assert login_response.status_code == 401
    assert 'refresh_token' not in login_response.cookies


async def test_refresh_session(async_client, logged_user):
    refresh_token = generate_refresh_token(logged_user.id)
    async_client.cookies['refresh_token'] = refresh_token

    refresh_response = await async_client.post('/auth/refresh')
    assert refresh_response.status_code == 200

    assert refresh_response.json()['token_type'] == 'bearer'


async def test_fail_refresh_session_invalid_token(
    async_client, logged_user, faker
):
    async_client.cookies['refresh_token'] = faker.password()
    refresh_response = await async_client.post('/auth/refresh')
    assert refresh_response.status_code == 401
