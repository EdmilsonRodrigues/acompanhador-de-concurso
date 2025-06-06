import json
from pathlib import Path

import factory
import faker
import pytest

from serviço_scraper.dtos.conteúdo import ConteúdoCruDTO, ConteúdoDTO

fake = faker.Faker()


tipos = json.load(Path('arquivos', 'tipos.json').open())


class FakeConteúdoCruDTO(factory.Factory):
    class Meta:
        model = ConteúdoCruDTO

    pubName = factory.Faker('name')
    urlTitle = factory.LazyAttribute(
        lambda o: o.title.lower().replace(' ', '-')
    )
    numberPage = factory.Faker('pyint')
    subTitulo = ''
    titulo = ''
    title = factory.Faker('sentence')
    pubDate = factory.Faker('date', pattern='%d/%m/%Y')
    content = factory.Faker('text', max_nb_chars=100)
    editionNumber = factory.Faker('pyint')
    hierarchyLevelSize = factory.Faker('pyint', max_value=5)
    artType = factory.Faker('sentence')
    pubOrder = factory.Faker('pyint')
    hierarchyList = factory.LazyAttribute(
        lambda o: [fake.word() for _ in range(o.hierarchyLevelSize)]
    )
    hierarchyStr = factory.LazyAttribute(lambda o: '/'.join(o.hierarchyList))


class FakeConteúdoDTO(factory.Factory):
    class Meta:
        model = ConteúdoDTO

    url = factory.Faker('url')
    título = factory.Faker('text')
    conteúdo = factory.Faker('text')
    hierarquia = factory.Faker('text')
    tipo = factory.LazyFunction(lambda: fake.random_element(tipos))
    data_publicação = factory.Faker('date')
    tags = []


@pytest.fixture
def gerador_conteúdo_cru():
    return FakeConteúdoCruDTO.create


@pytest.fixture
def gerador_conteúdo():
    return FakeConteúdoDTO.create
