import pytest

from backend_service.models.search_alert_model import SearchAlertPublic

pytestmark = pytest.mark.anyio


@pytest.fixture
def faker_locale():
    return ['pt_BR']


async def test_get_search_alerts(
    async_client, logged_user_search_alerts, access_token, faker
):
    limit = faker.pyint(min_value=1, max_value=10)
    offset = faker.pyint(min_value=0, max_value=10 - limit)
    expected = [
        SearchAlertPublic(**alert.model_dump()).model_dump()
        for alert in logged_user_search_alerts[offset : offset + limit]
    ]

    response = await async_client.get(
        '/search-alerts/',
        headers={'Authorization': access_token},
        params={'limit': limit, 'offset': offset},
    )

    assert response.status_code == 200
    assert response.json() == expected


async def test_get_no_search_alerts(
    async_client, logged_user_search_alerts, access_token, faker, orm_session
):
    for alert in logged_user_search_alerts:
        alert.user_id += 1
        orm_session.add(alert)
    orm_session.commit()

    response = await async_client.get(
        '/search-alerts/', headers={'Authorization': access_token}
    )

    assert response.status_code == 200
    assert response.json() == []


async def test_get_search_alert(
    async_client, logged_user_search_alert, access_token
):
    expected = SearchAlertPublic(
        **logged_user_search_alert.model_dump()
    ).model_dump()
    response = await async_client.get(
        f'/search-alerts/{logged_user_search_alert.id}',
        headers={'Authorization': access_token},
    )

    assert response.status_code == 200
    assert response.json() == expected


async def test_fail_get_search_alert_no_search_alert(
    async_client, logged_user_search_alert, access_token, orm_session
):
    logged_user_search_alert.user_id += 1
    orm_session.add(logged_user_search_alert)
    orm_session.commit()

    response = await async_client.get(
        f'/search-alerts/{logged_user_search_alert.id}',
        headers={'Authorization': access_token},
    )

    assert response.status_code == 404


async def test_create_search_alert(
    async_client, access_token, faker, logged_user, faker_locale
):
    area = faker.job()
    state = faker.estado_sigla()

    response = await async_client.post(
        '/search-alerts/',
        json={'area': area, 'state': state},
        headers={'Authorization': access_token},
    )

    assert response.status_code == 200
    assert response.json()['area'] == area
    assert response.json()['state'] == state
    assert response.json()['id']
    assert response.json()['user_id'] == logged_user.id


async def test_delete_search_alert(
    async_client, access_token, logged_user_search_alert
):
    response = await async_client.delete(
        f'/search-alerts/{logged_user_search_alert.id}',
        headers={'Authorization': access_token},
    )

    assert response.status_code == 204


async def test_fail_delete_search_alert_no_search_alert(
    async_client, access_token, logged_user_search_alert, orm_session
):
    logged_user_search_alert.user_id += 1
    orm_session.add(logged_user_search_alert)
    orm_session.commit()

    response = await async_client.delete(
        f'/search-alerts/{logged_user_search_alert.id}',
        headers={'Authorization': access_token},
    )

    assert response.status_code == 404
