from serviço_scraper.interfaces.categorizador import InterfaceCategorizador


class CategorizadorTeste(InterfaceCategorizador):
    def categorizar(self, parser): ...


def test_categorizador_init():
    async def gerador():
        yield

    categorizador = CategorizadorTeste(gerador)

    categorizador.gerador == gerador
