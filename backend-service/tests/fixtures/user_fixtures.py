from copy import replace

import factory
import pytest

from backend_service.models.user_model import User
from backend_service.services.auth_service import (
    generate_auth_token,
    hash_password,
)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = None
    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def logged_user(user, orm_session) -> User:
    old_password = user.password
    user.password = hash_password(user.password)
    orm_session.add(user)
    orm_session.commit()
    orm_session.refresh(user)
    return replace(user, password=old_password)


@pytest.fixture
def access_token(logged_user) -> str:
    token = generate_auth_token(logged_user.id)
    return 'Bearer ' + token
