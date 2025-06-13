from typing import Annotated

from sqlmodel import Field, SQLModel


class SubscriptionBase(SQLModel):
    customer_id: Annotated[str, Field(description='Stripe customer id')]
    subscription_id: Annotated[
        str, Field(description='Stripe subscription id')
    ]


class Subscription(SubscriptionBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    user_id: Annotated[int, Field(foreign_key='user.id', index=True)]


class SubscriptionPublic(SubscriptionBase):
    id: Annotated[int, Field()]
