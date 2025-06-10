import pytest

from backend_service.main import app, lifespan

pytest_plugins = ['tests.fixtures.user_fixtures']


@pytest.fixture
def anyio_backend():
    return ('asyncio', {'use_uvloop': True})


@pytest.fixture
async def async_client():
    import httpx

    async with lifespan(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url='http://test'
        ) as client:
            yield client
