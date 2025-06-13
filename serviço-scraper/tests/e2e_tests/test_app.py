from datetime import date

import pytest

from serviço_scraper.app import main
from serviço_scraper.config import Config
from serviço_scraper.serviços.repositório_sqlalchemy import (
    Conteúdo,
    ConteúdoRepositório,
)
from serviço_scraper.sessions import get_motor

DATA_TESTE = date(2025, 5, 15)


@pytest.mark.anyio
@pytest.mark.e2e
async def test_app():
    Config.DATA = DATA_TESTE
    motor = get_motor()

    await main()

    abridor_de_sessão = ConteúdoRepositório(motor).open

    with abridor_de_sessão() as sessão:
        total_conteúdos = sessão.query(Conteúdo).count()

    assert total_conteúdos
