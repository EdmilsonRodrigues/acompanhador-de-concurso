from fastapi import APIRouter

from ..dependencies.client_session_dependencies import ClientSessionDependency
from ..dependencies.services_dependencies import ORMSessionDependency
from ..models.user_model import UserPublic, UserUpdate

router = APIRouter(
    prefix='/me',
    tags=['users', 'me'],
    responses={404: {'description': 'User not found'}},
)


@router.get('/', response_model=UserPublic)
async def read_user(client_session: ClientSessionDependency):
    return client_session


@router.patch('/', response_model=UserPublic)
def update_user(
    user: UserUpdate,
    client_session: ClientSessionDependency,
    orm_session: ORMSessionDependency,
):
    user_data = user.model_dump(exclude_unset=True)
    client_session.sqlmodel_update(user_data)

    orm_session.add(client_session)
    orm_session.commit()
    orm_session.refresh(client_session)

    return client_session


@router.delete('/', status_code=204)
def delete_user(
    client_session: ClientSessionDependency, orm_session: ORMSessionDependency
) -> None:
    client_session.deactivate()
    orm_session.add(client_session)
    orm_session.commit()
