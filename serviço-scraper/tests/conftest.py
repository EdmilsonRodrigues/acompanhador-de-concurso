import sys

import pytest

print(sys.path)

pytest_plugins = [
    'tests.fixtures.conteúdo_fixtures',
]


@pytest.fixture
def anyio_backend():
    return 'asyncio'
