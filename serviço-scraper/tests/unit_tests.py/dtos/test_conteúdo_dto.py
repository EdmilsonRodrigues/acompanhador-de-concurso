from datetime import date
from urllib.parse import urlparse

from serviço_scraper.dtos.conteúdo import FORMATO_DATA_DOU, ConteúdoDTO


def test_from_dado_cru(gerador_conteúdo_cru):
    conteúdo_cru = gerador_conteúdo_cru()

    dado_parseado = ConteúdoDTO.from_dado_cru(conteúdo_cru)

    assert isinstance(dado_parseado, ConteúdoDTO)

    assert urlparse(dado_parseado.url).scheme == 'https'
    assert conteúdo_cru.urlTitle in dado_parseado.url

    assert conteúdo_cru.title == dado_parseado.título

    assert isinstance(dado_parseado.data_publicação, date)
    assert (
        dado_parseado.data_publicação.strftime(FORMATO_DATA_DOU)
        == conteúdo_cru.pubDate
    )

    assert dado_parseado.tipo == conteúdo_cru.artType
    assert dado_parseado.conteúdo == conteúdo_cru.content
    assert dado_parseado.hierarquia == conteúdo_cru.hierarchyList
