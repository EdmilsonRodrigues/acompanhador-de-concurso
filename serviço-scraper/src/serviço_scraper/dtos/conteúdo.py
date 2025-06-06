from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Annotated, NamedTuple, Self

URL_BASE_ARTIGOS_DOU = 'https://www.in.gov.br/web/dou/-/'
FORMATO_DATA_DOU = '%d/%m/%Y'


class ConteúdoCruDTO(NamedTuple):
    pubName: str
    urlTitle: str
    numberPage: str
    subTitulo: str
    titulo: str
    title: str
    pubDate: str
    content: str
    editionNumber: str
    hierarchyLevelSize: int
    artType: str
    pubOrder: str
    hierarchyStr: str
    hierarchyList: list[str]


@dataclass
class ConteúdoDTO:
    url: str
    título: str
    conteúdo: str
    hierarquia: list[str]
    tipo: str
    data_publicação: date
    tags: Annotated[list[str], field(default_factory=list)]
    estado: str = 'não avaliado'

    @classmethod
    def from_dado_cru(cls, dado_cru: ConteúdoCruDTO) -> Self:
        """
        Cria um ConteúdoDTO a partir de um ConteúdoCruDTO.

        Args:
            dado_cru (ConteúdoCruDTO): O objeto com os dados crus.

        Returns:
            ConteúdoDTO: O objeto com os dados parseados.
        """
        return cls(
            url=URL_BASE_ARTIGOS_DOU + dado_cru.urlTitle,
            título=dado_cru.title or dado_cru.titulo,
            conteúdo=dado_cru.content,
            hierarquia=dado_cru.hierarchyList,
            tipo=dado_cru.artType,
            data_publicação=datetime.strptime(
                dado_cru.pubDate, FORMATO_DATA_DOU
            ).date(),
            tags=[],
        )
