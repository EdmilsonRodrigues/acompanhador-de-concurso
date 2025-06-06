from serviço_scraper.interfaces.repositório import InterfaceRepositório


class RepositórioTeste(InterfaceRepositório):
    def __init__(self):
        self.aberto = False

    async def aopen(self):
        self.aberto = True

    async def aclose(self):
        self.aberto = False

    async def salvar(self):
        pass

    async def salvar_todos(self):
        pass


async def test_interface_repositório_contexto(anyio_backend):
    repositório = RepositórioTeste()

    assert not repositório.aberto

    async with repositório:
        assert repositório.aberto

    assert not repositório.aberto
