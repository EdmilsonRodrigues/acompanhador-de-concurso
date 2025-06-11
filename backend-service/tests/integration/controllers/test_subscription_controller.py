import pytest

from backend_service.models.subscription_model import SubscriptionPublic

pytestmark = pytest.mark.anyio


@pytest.fixture
def test_lookup_key():
    return 'test_standard_month'


@pytest.fixture
def test_customer_id():
    return 'cus_STjoMI3zIXiqjx'


async def test_get_subscription(
    async_client, logged_user, access_token, logged_user_subscription
):
    expected = SubscriptionPublic(
        **logged_user_subscription.model_dump()
    ).model_dump()

    response = await async_client.get(
        '/subscriptions/me', headers={'Authorization': access_token}
    )

    assert response.status_code == 200
    assert response.json() == expected


async def test_fail_get_subscription_not_found(async_client, access_token):
    response = await async_client.get(
        '/subscriptions/me', headers={'Authorization': access_token}
    )

    assert response.status_code == 404


async def test_get_checkout_session(
    async_client, access_token, test_lookup_key
):
    response = await async_client.post(
        '/subscriptions/checkout',
        headers={'Authorization': access_token},
        json={'lookup_key': test_lookup_key},
    )

    assert response.status_code == 303
    assert response.headers['Location'].startswith(
        'https://checkout.stripe.com'
    )


async def test_get_customer_portal(
    async_client,
    access_token,
    test_customer_id,
    orm_session,
    logged_user_subscription,
):
    logged_user_subscription.customer_id = test_customer_id
    orm_session.add(logged_user_subscription)
    orm_session.commit()

    response = await async_client.get(
        '/subscriptions/portal',
        headers={'Authorization': access_token},
    )

    assert response.status_code == 303
    assert response.headers['Location'].startswith(
        'https://billing.stripe.com'
    )
