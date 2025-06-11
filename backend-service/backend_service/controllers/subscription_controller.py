from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse

from ..dependencies.client_session_dependencies import ClientSessionDependency
from ..dependencies.models_dependencies import SubscriptionDependency
from ..models.subscription_model import SubscriptionPublic
from ..services.stripe_service import (
    create_checkout_session,
    create_customer_portal_session,
    find_stripe_prices,
)

router = APIRouter(
    prefix='/subscriptions',
    tags=['subscription'],
    responses={404: {'description': 'Subscription not found'}},
)


@router.post('/checkout', response_class=RedirectResponse)
def checkout_session(
    lookup_key: Annotated[str, Body(embed=True)],
    client_session: ClientSessionDependency,
):
    prices = find_stripe_prices(lookup_key)

    checkout_session = create_checkout_session(
        prices.data[0], client_session.id
    )

    return RedirectResponse(url=checkout_session.url, status_code=303)


@router.get('/portal', response_class=RedirectResponse)
def customer_portal(subscription: SubscriptionDependency):
    portal_session = create_customer_portal_session(subscription.customer_id)

    return RedirectResponse(url=portal_session.url, status_code=303)


@router.get('/me', response_model=SubscriptionPublic)
async def get_subscription(subscription: SubscriptionDependency):
    return subscription
