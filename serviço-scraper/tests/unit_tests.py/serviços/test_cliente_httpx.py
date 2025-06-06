import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import pytest

from serviço_scraper.serviços.cliente_httpx import ClienteHTTPX


@pytest.fixture
def servidor():
    return HTTPServer(('127.0.0.1', 8000), BaseHTTPRequestHandler)


@pytest.fixture
def servidor_thread(servidor):
    servidor_thread = threading.Thread(target=servidor.serve_forever)
    servidor_thread.start()
    yield servidor
    servidor.shutdown()
    servidor.server_close()
    servidor_thread.join()


@pytest.mark.anyio
async def test_cliente_httpx(servidor_thread):
    async with ClienteHTTPX() as cliente:
        assert (
            await cliente.get(
                urlparse(
                    f'http://{servidor_thread.server_address[0]}:{servidor_thread.server_address[1]}'
                )
            )
        ).text
