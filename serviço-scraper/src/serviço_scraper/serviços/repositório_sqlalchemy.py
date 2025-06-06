from datetime import date
from typing import Self

from sqlalchemy import Date, Engine, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker

from ..dtos.conteúdo import ConteúdoDTO
from ..interfaces.repositório import (
    InterfaceRepositório,
    InterfaceRepositórioDTO,
)
from ..sessions import Base
from .utils import implementa

ESTADO_PADRÃO = 'não avaliado'


class Conteúdo(Base):
    __tablename__ = 'publicacao'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False, index=True
    )
    título: Mapped[str] = mapped_column(String(200), nullable=False)
    categoria: Mapped[str] = mapped_column(String(15), nullable=False)
    conteúdo: Mapped[str] = mapped_column(String(403), nullable=False)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    data_publicação: Mapped[date] = mapped_column(Date, nullable=False)
    tags: Mapped[list[str]] = mapped_column(
        postgresql.ARRAY(String(100)), nullable=False
    )
    hierarquia: Mapped[list[str]] = mapped_column(
        postgresql.ARRAY(String(100)), nullable=False
    )
    estado: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return (
            f"<Conteúdo(id={self.id}, título='{self.título[:30]}...', "
            f"url='{self.url[:30]}...', categoria='{self.categoria}', "
            f'data_publicação={self.data_publicação}, tags={self.tags})>'
        )

    @classmethod
    @implementa(InterfaceRepositórioDTO.from_dado)
    def from_dado(cls, categoria: str, conteúdo: ConteúdoDTO) -> Self:
        return cls(
            url=conteúdo.url,
            título=conteúdo.título,
            categoria=categoria,
            conteúdo=conteúdo.conteúdo,
            tipo=conteúdo.tipo,
            data_publicação=conteúdo.data_publicação,
            tags=conteúdo.tags,
            hierarquia=conteúdo.hierarquia,
            estado=ESTADO_PADRÃO,
        )


class ConteúdoRepositório(InterfaceRepositório):
    sessão: Session | None = None

    def __init__(self, motor: Engine):
        super().__init__(motor)

        Base.metadata.create_all(self.motor)

        self.open = sessionmaker(autoflush=False, bind=self.motor)
        self.sessão = None

    async def aopen(self):
        self.sessão = self.open()
        return self

    async def aclose(self):
        self.sessão.close()
        self.sessão = None

    @implementa(InterfaceRepositório.salvar_todos)
    async def salvar_todos(
        self, conteúdos: list[Conteúdo] | dict[str, list[Conteúdo]]
    ) -> None:
        if self.sessão is None:
            raise RuntimeError(
                'A sessão precisa ser aberta para executar essa função.'
            )

        self.sessão.add_all(conteúdos)

        self.sessão.commit()
