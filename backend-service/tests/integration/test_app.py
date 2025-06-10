import pytest

pytestmark = pytest.mark.anyio


async def test_app(async_client):
    response = await async_client.get('/')
    assert response.status_code == 200
