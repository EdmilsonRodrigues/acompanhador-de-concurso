from typing import Annotated

from fastapi import APIRouter, Header, Request
from pydantic import AliasPath, BaseModel, Field

from ..dependencies.services_dependencies import ORMSessionDependency
from ..models.subscription_model import Subscription
from ..services.logging_service import get_logger
from ..services.stripe_service import get_webhook_event

router = APIRouter(prefix='/stripe', tags=['stripe'], include_in_schema=False)
logger = get_logger()


class CheckoutSessionCompletedDTO(BaseModel):
    customer_id: Annotated[str, Field(alias='customer')]
    subscription_id: Annotated[str, Field(alias='subscription')]
    user_id: Annotated[
        int, Field(validation_alias=AliasPath('metadata', 'user_id'))
    ]


EVENT_DTO_MAPPER = {'checkout.session.completed': CheckoutSessionCompletedDTO}


@router.post('/webhook')
async def webhook_received(
    request: Request,
    signature: Annotated[str, Header(alias='stripe-signature')],
    orm_session: ORMSessionDependency,
):
    event = get_webhook_event(await request.body(), signature)

    data = event['data']
    event_type = event['type']
    data_object = data['object']

    parsed_data = EVENT_DTO_MAPPER[event_type](**data_object)

    logger.info({
        'message': 'Webhook received',
        'event_type': event_type,
        'parsed_data': parsed_data.model_dump(),
    })

    match event_type:
        case 'checkout.session.completed':
            subscription = Subscription(**parsed_data.model_dump())
            orm_session.add(subscription)
            orm_session.commit()
        case 'customer.subscription.trial_will_end':  # TODO
            ...  # handle trial will end
        case 'customer.subscription.deleted':  # TODO
            ...  # handle subscription deleted

    return {'status': 'success'}
