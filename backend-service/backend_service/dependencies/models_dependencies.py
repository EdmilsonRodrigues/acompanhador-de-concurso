from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from ..exceptions.controller_exceptions import SubscriptionNotFoundException
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


SubscriptionDependency = Annotated[Subscription, Depends(_get_subscription)]
