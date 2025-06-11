import pytest

from backend_service.dependencies.models_dependencies import _get_subscription
from backend_service.exceptions.controller_exceptions import (
    SubscriptionNotFoundException,
)

pytestmark = pytest.mark.anyio


async def test_get_subscription(
    logged_user_subscription, logged_user, orm_session
):
    subscription = await _get_subscription(logged_user, orm_session)

    assert subscription == logged_user_subscription


async def test_fail_get_subscription_no_subscription_to_user(
    logged_user, orm_session
):
    with pytest.raises(SubscriptionNotFoundException):
        await _get_subscription(logged_user, orm_session)
