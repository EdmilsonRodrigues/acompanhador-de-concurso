import logging
from collections.abc import AsyncGenerator, Generator
from datetime import date
from urllib.parse import ParseResult, urlparse

import bs4
import orjson

from ..dtos.conteúdo import ConteúdoCruDTO, ConteúdoDTO
from ..interfaces.scraper import InterfaceScraper
from .utils import implementa

logger = logging.getLogger()


class DOUScraper(InterfaceScraper):
    URL_BASE = 'https://www.in.gov.br/leiturajornal?data={data}&secao=do3'
    TIMEOUT = 120

    @implementa(InterfaceScraper.scrape_dia)
    async def scrape_dia(self, data: date) -> AsyncGenerator['ConteúdoDTO']:
        url = self.URL_BASE.format(data=self._formatar_data(data))
        async for conteúdo in self._scrape_url(urlparse(url)):
            yield conteúdo

    async def _scrape_url(
        self, url: ParseResult
    ) -> AsyncGenerator['ConteúdoDTO']:
        """
        Realiza a ação de scraping de uma url especifica no Diário Oficial
            da União e retorna a resposta parseada em um gerador do DTO
            para conteúdo.

        Args:
            url (ParseResult): URL a ser buscada.

        Returns:
            AsyncGenerator['ConteúdoDTO']: Gerador de ConteúdoDTO com os
                conteúdos parseados.
        """
        logger.info(f'Scraping {url}')

        dados_crus = await self._pegar_dados_crus_dos_itens_publicados(url)

        for dado_cru in self._parsear_dados_crus(dados_crus):
            yield ConteúdoDTO.from_dado_cru(dado_cru)

    def _formatar_data(self, data: date) -> str:
        return data.strftime('%d-%m-%Y')

    async def _get_html(self, url: ParseResult) -> str:
        return (await self.cliente.get(url, timeout=self.TIMEOUT)).text

    async def _pegar_dados_crus_dos_itens_publicados(
        self, url: ParseResult
    ) -> list[dict]:
        sopa = bs4.BeautifulSoup(await self._get_html(url), 'html.parser')
        params = sopa.find('script', {'id': 'params'})
        if params is None:
            raise ValueError('A página do Diário Oficial da União mudou.')

        return orjson.loads(params.text)['jsonArray']

    @staticmethod
    def _parsear_dados_crus(
        dados_crus: list[dict],
    ) -> Generator['ConteúdoCruDTO']:
        for conteudo in dados_crus:
            yield ConteúdoCruDTO(**conteudo)
