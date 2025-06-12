import factory
import pytest

from backend_service.models.search_alert_model import SearchAlert


class SearchAlertFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SearchAlert

    id = None
    state = factory.Faker('estado_sigla', locale='pt_BR')
    area = factory.Faker('job', locale='pt_BR')
    user_id = 1


@pytest.fixture
def search_alert() -> SearchAlert:
    return SearchAlertFactory.build()


@pytest.fixture
def search_alerts() -> list[SearchAlert]:
    return SearchAlertFactory.build_batch(10)


@pytest.fixture
async def logged_user_search_alert(
    search_alert, logged_user, orm_session
) -> SearchAlert:
    search_alert.user_id = logged_user.id
    orm_session.add(search_alert)
    orm_session.commit()
    orm_session.refresh(search_alert)
    return search_alert


@pytest.fixture
async def logged_user_search_alerts(
    search_alerts, logged_user, orm_session
) -> list[SearchAlert]:
    for search_alert in search_alerts:
        search_alert.user_id = logged_user.id
        orm_session.add(search_alert)
    orm_session.commit()
    for search_alert in search_alerts:
        orm_session.refresh(search_alert)
    return search_alerts
