from fastapi import APIRouter

from ..dependencies.client_session_dependencies import ClientSessionDependency
from ..dependencies.services_dependencies import ORMSessionDependency
from ..exceptions.controller_exceptions import InvalidDataException
from ..exceptions.services_exceptions import UnmatchedPasswordException
from ..models.user_model import UserPasswordUpdate, UserPublic, UserUpdate

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
    updated_data: UserUpdate | UserPasswordUpdate,
    client_session: ClientSessionDependency,
    orm_session: ORMSessionDependency,
):
    try:
        client_session.update(updated_data)
    except UnmatchedPasswordException as exc:
        raise InvalidDataException(str(exc)) from exc

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
