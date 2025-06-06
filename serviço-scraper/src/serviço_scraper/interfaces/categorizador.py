from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Callable

from ..dtos.conteúdo import ConteúdoDTO


class InterfaceCategorizador(ABC):
    def __init__(self, gerador: AsyncGenerator[ConteúdoDTO]):
        self.gerador = gerador

    @abstractmethod
    def categorizar[T](
        self, parser: Callable[[str, ConteúdoDTO], T]
    ) -> AsyncGenerator[T]:
        """
        Categoriza os conteúdos de um gerador assíncrono de ConteúdoDTO,
        parseando-os no processo.

        Args:
            parser (Callable[[str, ConteúdoDTO], T], optional): Função para
                parsear os conteúdos. O primeiro argumento a ser recebido deve
                ser a categoria e o segundo o conteúdo que pertence a ela.

        Returns:
            Generator[T]: Gerador de conteúdos categorizados e parseados para T
        """
        ...
