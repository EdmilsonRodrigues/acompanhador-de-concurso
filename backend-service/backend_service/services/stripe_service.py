from typing import AnyStr

import stripe

from ..config import Settings, StripeSettings
from ..exceptions.services_exceptions import (
    FailedCreatingCheckoutSessionException,
    FailedCreatingPortalSessionException,
    FailedGettingWebhookException,
    FailedListingStripePricesException,
)

stripe.api_key = StripeSettings().SECRET_KEY
webhook_secret = StripeSettings().WEBHOOK_SECRET


def find_stripe_prices(lookup_key: str):
    try:
        prices = stripe.Price.list(
            lookup_keys=[lookup_key], expand=['data.product']
        )
    except Exception as exc:  # pragma: no cover
        raise FailedListingStripePricesException from exc

    return prices


def create_checkout_session(price: stripe.APIResource, user_id: int):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='subscription',
            success_url=Settings().FRONTEND_URL
            + '/subscriptions/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=Settings().FRONTEND_URL + '/subscriptions/cancel',
            metadata={'user_id': user_id},
        )
    except Exception as exc:  # pragma: no cover
        raise FailedCreatingCheckoutSessionException from exc
    return checkout_session


def create_customer_portal_session(customer_id: str) -> stripe.APIResource:
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=Settings().FRONTEND_URL,
        )
    except Exception as exc:  # pragma: no cover
        raise FailedCreatingPortalSessionException from exc
    return portal_session


def get_webhook_event(payload: AnyStr, signature_header: str):
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature_header,
            secret=webhook_secret,
        )
    except Exception as exc:  # pragma: no cover
        raise FailedGettingWebhookException from exc

    return event
