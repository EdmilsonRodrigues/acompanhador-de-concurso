import hashlib
import hmac
import json
import time
from pathlib import Path

import orjson
import pytest
from sqlmodel import select

from backend_service.models.subscription_model import Subscription
from backend_service.services import stripe_service

pytestmark = pytest.mark.anyio
MIN_USER_ID = 1


def generate_stripe_signature(payload, secret, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())

    signed_payload = f'{timestamp}.{payload}'

    hashed = hmac.new(
        secret.encode('utf-8'), signed_payload.encode('utf-8'), hashlib.sha256
    ).hexdigest()

    return f't={timestamp},v1={hashed}'


@pytest.fixture
def sample_checkout_session_completed():
    path = Path('tests/fixtures/sample_checkout_session_completed.json')
    with path.open(encoding='utf-8') as f:
        data = orjson.loads(f.read())

    request = {'type': 'checkout.session.completed', 'data': data}

    return request


async def test_stripe_webhook(
    async_client,
    sample_checkout_session_completed,
    faker,
    monkeypatch,
    orm_session,
):
    webhook_secret = faker.password()
    monkeypatch.setattr(stripe_service, 'webhook_secret', webhook_secret)

    user_id = faker.pyint(min_value=MIN_USER_ID)

    sample_checkout_session_completed['data']['object']['metadata'][
        'user_id'
    ] = str(user_id)

    signature = generate_stripe_signature(
        json.dumps(sample_checkout_session_completed, separators=(',', ':')),
        webhook_secret,
    )

    response = await async_client.post(
        '/stripe/webhook',
        json=sample_checkout_session_completed,
        headers={'Stripe-Signature': signature},
    )

    statement = select(Subscription).where(Subscription.user_id == user_id)
    subscription = orm_session.exec(statement).one_or_none()

    assert response.status_code == 200
    assert subscription
