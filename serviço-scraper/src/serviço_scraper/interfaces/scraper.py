from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from datetime import date

from ..dtos.conteúdo import ConteúdoDTO
from .cliente_http import InterfaceClienteHTTP


class InterfaceScraper(ABC):
    def __init__(self, cliente: InterfaceClienteHTTP):
        self.cliente = cliente

    @abstractmethod
    async def scrape_dia(cls, data: date) -> AsyncGenerator[ConteúdoDTO]:
        """
        Realiza a ação de scraping de um dia específico no Diário Oficial
            da União e retorna a resposta parseada em um gerador do DTO
            para conteúdo.

        Args:
            data (date): Data a ser buscada.

        Returns:
            AsyncGenerator['ConteúdoDTO']: Gerador de ConteúdoDTO com os
                conteúdos parseados.
        """
        ...
