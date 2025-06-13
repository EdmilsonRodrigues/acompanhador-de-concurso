import asyncio

from .config import Config
from .interfaces.categorizador import InterfaceCategorizador
from .interfaces.cliente_http import InterfaceClienteHTTP
from .interfaces.repositório import (
    InterfaceRepositório,
    InterfaceRepositórioDTO,
)
from .interfaces.scraper import InterfaceScraper
from .serviços.categorizador_tipo import CategorizadorTipo
from .serviços.cliente_httpx import ClienteHTTPX
from .serviços.dou_scraper import DOUScraper
from .serviços.repositório_sqlalchemy import Conteúdo, ConteúdoRepositório
from .sessions import get_motor


async def _main(
    ClienteHTTP: type[InterfaceClienteHTTP],
    Scraper: type[InterfaceScraper],
    Categorizador: type[InterfaceCategorizador],
    Repositório: type[InterfaceRepositório],
    RepositórioDTO: type[InterfaceRepositórioDTO],
):
    async with ClienteHTTP() as cliente:
        data = Config.DATA
        if data.weekday() in [5, 6]:
            return

        scraper = Scraper(cliente)
        conteúdos = scraper.scrape_dia(data)

        categorizador = Categorizador(conteúdos)
        gerador_conteudos_categorizados = categorizador.categorizar(
            parser=RepositórioDTO.from_dado
        )

        async with Repositório(get_motor()) as repositório:
            await repositório.salvar_todos([
                conteúdo async for conteúdo in gerador_conteudos_categorizados
            ])


async def main():
    await _main(
        ClienteHTTP=ClienteHTTPX,
        Scraper=DOUScraper,
        Repositório=ConteúdoRepositório,
        Categorizador=CategorizadorTipo,
        RepositórioDTO=Conteúdo,
    )


if __name__ == '__main__':
    asyncio.run(main())
