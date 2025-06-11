from contextlib import contextmanager
from functools import cache

import httpx
import pytest
from sqlmodel import Session, StaticPool, create_engine

from backend_service.dependencies.services_dependencies import _get_orm_session
from backend_service.main import app
from backend_service.services.database_service import (
    create_db_and_tables,
    get_engine,
)

pytest_plugins = [
    'tests.fixtures.user_fixtures',
    'tests.fixtures.subscription_fixtures',
]


@pytest.fixture
def anyio_backend():
    return ('asyncio', {'use_uvloop': True})


def get_orm_session() -> Session:
    engine = get_in_memory_client_engine()
    with Session(engine) as session:
        yield session


@pytest.fixture
async def orm_session() -> Session:
    with contextmanager(get_orm_session)() as session:
        yield session


@pytest.fixture
async def async_client() -> httpx.AsyncClient:
    app.dependency_overrides[_get_orm_session] = get_orm_session
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client


@pytest.fixture
async def create_tables() -> None:
    engine = get_engine()
    create_db_and_tables(engine)


@cache
def get_in_memory_client_engine() -> None:
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    create_db_and_tables(engine)
    return engine
