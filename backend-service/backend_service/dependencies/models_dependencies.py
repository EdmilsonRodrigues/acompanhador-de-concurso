from typing import Annotated

from fastapi import Depends, Path, Query
from sqlmodel import select

from ..exceptions.controller_exceptions import (
    SearchAlertNotFoundException,
    SubscriptionNotFoundException,
)
from ..models.search_alert_model import SearchAlert
from ..models.subscription_model import Subscription
from .client_session_dependencies import ClientSessionDependency
from .services_dependencies import ORMSessionDependency


async def _get_subscription(
    client_session: ClientSessionDependency, orm_session: ORMSessionDependency
):
    statement = select(Subscription).where(
        Subscription.user_id == client_session.id
    )
    subscription = orm_session.exec(statement).one_or_none()
    if subscription is None:
        raise SubscriptionNotFoundException
    return subscription


async def _get_search_alerts(
    client_session: ClientSessionDependency,
    orm_session: ORMSessionDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    statement = (
        select(SearchAlert)
        .where(SearchAlert.user_id == client_session.id)
        .offset(offset)
        .limit(limit)
    )

    alerts = orm_session.exec(statement).all()

    return alerts


async def _get_search_alert(
    client_session: ClientSessionDependency,
    search_alert_id: Annotated[int, Path(ge=1)],
    orm_session: ORMSessionDependency,
):
    statement = (
        select(SearchAlert)
        .where(SearchAlert.id == search_alert_id)
        .where(SearchAlert.user_id == client_session.id)
    )

    alert = orm_session.exec(statement).one_or_none()
    if alert is None:
        raise SearchAlertNotFoundException

    return alert


SubscriptionDependency = Annotated[Subscription, Depends(_get_subscription)]
SearchAlertsDependency = Annotated[
    list[SearchAlert], Depends(_get_search_alerts)
]
SearchAlertDependency = Annotated[SearchAlert, Depends(_get_search_alert)]
