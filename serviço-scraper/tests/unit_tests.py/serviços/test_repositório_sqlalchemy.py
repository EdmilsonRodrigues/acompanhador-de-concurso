from serviço_scraper.serviços.repositório_sqlalchemy import (
    ESTADO_PADRÃO,
    Conteúdo,
)


def test_conteúdo_from_dado(gerador_conteúdo, faker):
    conteúdo = gerador_conteúdo()
    categoria = faker.word()

    conteúdo_parseado = Conteúdo.from_dado(categoria, conteúdo)

    assert isinstance(conteúdo_parseado, Conteúdo)
    assert conteúdo_parseado.categoria == categoria
    assert conteúdo_parseado.estado == ESTADO_PADRÃO
