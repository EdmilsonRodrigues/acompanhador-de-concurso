from urllib.parse import ParseResult

import httpx

from ..interfaces.cliente_http import InterfaceClienteHTTP, Response
from .utils import implementa


class ClienteHTTPX(InterfaceClienteHTTP):
    cliente: httpx.AsyncClient | None = None

    @implementa(InterfaceClienteHTTP.get)
    async def get(
        self, url: ParseResult, timeout: int = 10
    ) -> 'HTTPXResponse':
        if self.cliente is None:
            raise RuntimeError('O cliente HTTPX precisa ser aberto.')

        return HTTPXResponse(
            await self.cliente.get(url.geturl(), timeout=timeout)
        )

    @implementa(InterfaceClienteHTTP.open)
    async def open(self):
        self.cliente = httpx.AsyncClient(http2=True)

    @implementa(InterfaceClienteHTTP.close)
    async def close(self):
        await self.cliente.aclose()
        self.cliente = None


class HTTPXResponse(Response):
    def __init__(self, response: httpx.Response):
        self.response = response

    @property
    def text(self) -> str:
        return self.response.text
