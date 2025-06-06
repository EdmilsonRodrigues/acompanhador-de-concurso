from serviço_scraper.interfaces.cliente_http import InterfaceClienteHTTP


class ClienteHTTPTeste(InterfaceClienteHTTP):
    def __init__(self):
        self.aberto = False

    async def open(self):
        self.aberto = True

    async def close(self):
        self.aberto = False

    async def get(self):
        pass


async def test_interface_cliente_http_contexto(anyio_backend):
    cliente_http = ClienteHTTPTeste()
    assert not cliente_http.aberto

    async with cliente_http:
        assert cliente_http.aberto

    assert not cliente_http.aberto
