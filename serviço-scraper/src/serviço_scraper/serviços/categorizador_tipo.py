from collections.abc import AsyncGenerator, Callable

import orjson

from ..config import Config
from ..dtos.conteúdo import ConteúdoDTO
from ..interfaces.categorizador import InterfaceCategorizador
from .utils import implementa


class CategorizadorTipo(InterfaceCategorizador):
    @implementa(InterfaceCategorizador.categorizar)
    async def categorizar[T](
        self, parser: Callable[[str, ConteúdoDTO], T]
    ) -> AsyncGenerator[T]:
        categorias = {
            categoria: set(tipos)
            for categoria, tipos in orjson.loads(
                Config.CAMINHO_CATEGORIAS.read_text()
            ).items()
        }
        async for conteudo in self.gerador:
            for categoria, tipos in categorias.items():
                if conteudo.tipo in tipos:
                    if categoria == 'ignorar':
                        break

                    yield parser(categoria, conteudo)
                    break
            else:
                yield parser('outros', conteudo)
