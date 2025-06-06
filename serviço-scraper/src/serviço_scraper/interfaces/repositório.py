from abc import ABC, abstractmethod
from typing import Protocol, Self


class InterfaceRepositório[T: 'InterfaceRepositórioDTO'](ABC):
    def __init__(self, motor):
        self.motor = motor

    async def __aenter__(self):
        await self.aopen()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.aclose()

    @abstractmethod
    async def aopen(self):
        """
        Abre a sessão do repositório para execução de queries atômicas

        Returns:
            None
        """
        ...

    @abstractmethod
    async def aclose(self):
        """
        Fecha a sessão do repositório

        Returns:
            None
        """
        ...

    @abstractmethod
    async def salvar_todos(
        self, conteúdos: list[T] | dict[str, list[T]]
    ) -> None:
        """
        Salva todos os conteúdos no repositório

        Args:
            conteúdos (list[T] | dict[str, list[T]]): Conteúdos a serem salvos

        Returns:
            None
        """
        ...


class InterfaceRepositórioDTO(Protocol):
    @classmethod
    @abstractmethod
    def from_dado[T](cls, categoria: str, dado: T) -> Self:
        """
        Cria um DTO a partir de um dado

        Args:
            dado (T): Dado a ser convertido

        Returns:
            Self: Uma instância do DTO
        """
        ...
