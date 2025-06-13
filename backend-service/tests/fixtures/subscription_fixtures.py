import factory
import pytest

from backend_service.models.subscription_model import Subscription


class SubscriptionFactory(factory.Factory):
    class Meta:
        model = Subscription

    id = None
    customer_id = factory.Faker('uuid4')
    subscription_id = factory.Faker('uuid4')


@pytest.fixture
def subscription(logged_user) -> Subscription:
    return SubscriptionFactory(user_id=logged_user.id)


@pytest.fixture
async def logged_user_subscription(orm_session, subscription) -> Subscription:
    orm_session.add(subscription)
    orm_session.commit()
    orm_session.refresh(subscription)

    yield subscription

    orm_session.delete(subscription)
    orm_session.commit()
