from copy import replace

import pytest

from backend_service.dependencies.models_dependencies import (
    _get_search_alert,
    _get_search_alerts,
    _get_subscription,
)
from backend_service.exceptions.controller_exceptions import (
    SearchAlertNotFoundException,
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


async def test_get_search_alerts(
    logged_user_search_alerts, logged_user, orm_session, faker
):
    limit = faker.pyint(min_value=1, max_value=10)
    offset = faker.pyint(min_value=0, max_value=10 - limit)

    search_alerts = await _get_search_alerts(
        logged_user, orm_session, limit, offset
    )

    assert search_alerts == logged_user_search_alerts[offset : offset + limit]


async def test_get_search_alerts_no_search_alerts_to_user(
    logged_user, logged_user_search_alerts, orm_session, faker
):
    limit = faker.pyint(min_value=1, max_value=10)
    offset = faker.pyint(min_value=0, max_value=10 - limit)

    assert not await _get_search_alerts(
        replace(logged_user, id=logged_user.id + 1), orm_session, limit, offset
    )


async def test_get_search_alert(
    logged_user_search_alert, logged_user, orm_session
):
    search_alert = await _get_search_alert(
        logged_user, logged_user_search_alert.id, orm_session
    )

    assert search_alert == logged_user_search_alert


async def test_fail_get_search_alert_no_search_alert_to_user(
    logged_user, logged_user_search_alert, orm_session
):
    with pytest.raises(SearchAlertNotFoundException):
        await _get_search_alert(
            replace(logged_user, id=logged_user.id + 1),
            logged_user_search_alert.id,
            orm_session,
        )
