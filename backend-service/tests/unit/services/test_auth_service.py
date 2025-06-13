from datetime import UTC, datetime, timedelta

import freezegun
import pytest

from backend_service.config import Settings
from backend_service.exceptions.services_exceptions import (
    InvalidTokenException,
    UnmatchedPasswordException,
)
from backend_service.services.auth_service import (
    check_password,
    decode_jwt_token,
    generate_auth_token,
    generate_refresh_token,
    hash_password,
)

MIN_USER_ID = 1


def test_hash_password():
    password = 'password'

    hashed_password = hash_password(password)

    assert hashed_password
    assert hashed_password != password


def test_check_password():
    password = 'password'

    hashed_password = hash_password(password)

    check_password(password, hashed_password)


def test_fail_check_password():
    password = 'password'

    hashed_password = hash_password(password)

    with pytest.raises(UnmatchedPasswordException):
        check_password('wrong_password', hashed_password)


def test_generate_auth_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)

    token = generate_auth_token(user_id)
    assert token


def test_generate_refresh_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)

    token = generate_refresh_token(user_id)
    assert token


def test_decode_auth_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)
    now = datetime.now(UTC)
    not_expired_time = now + timedelta(seconds=Settings().EXPIRATION_TIME - 1)

    with freezegun.freeze_time(now):
        token = generate_auth_token(user_id)

    with freezegun.freeze_time(not_expired_time):
        assert decode_jwt_token(token) == user_id


def test_decode_refresh_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)
    now = datetime.now(UTC)
    not_expired_time = now + timedelta(
        seconds=Settings().REFRESH_TOKEN_EXPIRATION_TIME - 1
    )

    with freezegun.freeze_time(now):
        token = generate_refresh_token(user_id)

    with freezegun.freeze_time(not_expired_time):
        assert decode_jwt_token(token) == user_id


def test_decode_jwt_token_invalid_token(faker):
    token = faker.pystr()

    with pytest.raises(InvalidTokenException):
        decode_jwt_token(token)


def test_expired_auth_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)
    expired_time = datetime.now(UTC) + timedelta(
        seconds=Settings().EXPIRATION_TIME
    )

    token = generate_auth_token(user_id)

    with freezegun.freeze_time(expired_time):
        with pytest.raises(InvalidTokenException):
            decode_jwt_token(token)


def test_expired_refresh_token(faker):
    user_id = faker.pyint(min_value=MIN_USER_ID)
    expired_time = datetime.now(UTC) + timedelta(
        seconds=Settings().REFRESH_TOKEN_EXPIRATION_TIME
    )

    token = generate_refresh_token(user_id)

    with freezegun.freeze_time(expired_time):
        with pytest.raises(InvalidTokenException):
            decode_jwt_token(token)
