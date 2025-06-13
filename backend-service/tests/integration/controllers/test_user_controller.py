import pytest

from backend_service.models.user_model import UserPublic

pytestmark = pytest.mark.anyio


async def test_get_me(async_client, logged_user, access_token):
    expected = UserPublic(**logged_user.model_dump()).model_dump()
    response = await async_client.get(
        '/me/', headers={'Authorization': access_token}
    )
    assert response.status_code == 200

    assert response.json() == expected


@pytest.mark.filterwarnings('ignore')
async def test_update_me(async_client, logged_user, access_token, faker):
    field_to_update = faker.random_element(('name', 'email'))
    updated_field = getattr(faker, field_to_update)()

    expected = UserPublic(**logged_user.model_dump()).model_dump()
    expected[field_to_update] = updated_field

    response = await async_client.patch(
        '/me/',
        json={field_to_update: updated_field},
        headers={'Authorization': access_token},
    )
    assert response.status_code == 200

    assert response.json() == expected


async def test_delete_me(async_client, logged_user, access_token, orm_session):
    response = await async_client.delete(
        '/me/', headers={'Authorization': access_token}
    )
    assert response.status_code == 204

    response = await async_client.get(
        '/me/', headers={'Authorization': access_token}
    )
    assert response.status_code == 404
