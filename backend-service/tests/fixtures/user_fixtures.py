from contextlib import contextmanager
from copy import replace

import factory
import pytest

from backend_service.dependencies.services_dependencies import get_orm_session
from backend_service.models.user_model import User
from backend_service.services.auth_service import hash_password


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def logged_user(user):
    with contextmanager(get_orm_session)() as session:
        old_password = user.password
        user.password = hash_password(user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
        yield replace(user, password=old_password)
        session.delete(user)
        session.commit()
