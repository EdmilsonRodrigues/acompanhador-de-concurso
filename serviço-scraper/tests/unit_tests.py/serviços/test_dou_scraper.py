import json
from collections import namedtuple
from datetime import date

import pytest

from serviço_scraper.dtos.conteúdo import ConteúdoDTO
from serviço_scraper.interfaces.cliente_http import InterfaceClienteHTTP
from serviço_scraper.serviços.dou_scraper import DOUScraper


@pytest.fixture
def cliente():
    class ClienteTeste(InterfaceClienteHTTP):
        def __init__(self, conteúdos):
            self.conteúdos = conteúdos

        async def get(self, url, timeout=10):
            return namedtuple('TesteHTTPResponse', 'text')(f"""
            <script id="params">
                {{"jsonArray": {
                json.dumps([conteúdo._asdict() for conteúdo in self.conteúdos])
            }
                }}
            </script>
            """)

        async def close(self): ...
        async def open(self):
            return self

    return ClienteTeste


@pytest.mark.anyio
async def test_dou_scraper(cliente, gerador_conteúdo_cru):
    conteúdos = [gerador_conteúdo_cru() for _ in range(4)]
    scraper = DOUScraper(cliente(conteúdos))
    data = date.today()

    index = 0
    async for conteúdo in scraper.scrape_dia(data):
        assert conteúdo == ConteúdoDTO.from_dado_cru(conteúdos[index])
        index += 1
