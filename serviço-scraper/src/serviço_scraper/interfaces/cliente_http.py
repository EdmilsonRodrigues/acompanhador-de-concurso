from abc import ABC, abstractmethod
from urllib.parse import ParseResult


class InterfaceClienteHTTP(ABC):
    @abstractmethod
    async def get(self, url: ParseResult, timeout: int = 10) -> 'Response':
        """
        Faz uma requisição GET para a URL fornecida e retorna uma resposta.

        Args:
            url (ParseResult): A URL para a qual a requisição será feita.
            timeout (int, optional): O tempo limite em segundos para
                a requisição. Padrão é 10.

        Returns:
            Response: A resposta da requisição.
        """
        ...

    @abstractmethod
    async def open(self):
        """
        Abre a conexão do cliente HTTP.
        """
        ...

    @abstractmethod
    async def close(self):
        """
        Fecha a conexão do cliente HTTP.
        """
        ...

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class Response(ABC):
    @property
    @abstractmethod
    def text(self) -> str:
        """
        Retorna o conteúdo da resposta como uma string.

        Returns:
            str: O conteúdo da resposta.
        """
        ...
