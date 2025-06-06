import json
import random

import pytest
from faker import Faker

from serviço_scraper.config import Config
from serviço_scraper.serviços.categorizador_tipo import CategorizadorTipo


@pytest.fixture
def categorias():
    return json.load(Config.CAMINHO_CATEGORIAS.open())


@pytest.fixture
def gerador():
    async def gerador_conteúdo(conteudo):
        yield conteudo

    return gerador_conteúdo


@pytest.fixture
def parser():
    def categoria_e_conteúdo_parser(categoria, conteúdo):
        return (categoria, conteúdo)

    return categoria_e_conteúdo_parser


@pytest.mark.parametrize('categoria', ['licitação', 'concurso'])
async def test_categorizador_tipos_desejados(
    anyio_backend, gerador_conteúdo, categorias, categoria, gerador, parser
):
    conteúdo = gerador_conteúdo()
    conteúdo.tipo = random.choice(categorias[categoria])

    categorizador = CategorizadorTipo(gerador(conteúdo))
    async for categoria_e_conteúdo in categorizador.categorizar(parser):
        assert categoria_e_conteúdo == (categoria, conteúdo)


async def test_categorizador_tipos_ignorados(
    anyio_backend, gerador_conteúdo, categorias, gerador, parser
):
    conteúdo = gerador_conteúdo()
    conteúdo.tipo = random.choice(categorias['ignorar'])

    categorizador = CategorizadorTipo(gerador(conteúdo))
    async for categoria_e_conteúdo in categorizador.categorizar(parser):
        raise AssertionError(
            'Categoria e conteúdo não deveriam '
            f'existir: {categoria_e_conteúdo}'
        )


async def test_categorizador_outros_tipos(
    anyio_backend, gerador_conteúdo, categorias, gerador, parser
):
    conteúdo = gerador_conteúdo()
    conteúdo.tipo = Faker().word()

    categorizador = CategorizadorTipo(gerador(conteúdo))
    async for categoria_e_conteúdo in categorizador.categorizar(parser):
        assert categoria_e_conteúdo == ('outros', conteúdo)
