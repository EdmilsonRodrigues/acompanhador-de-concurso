from fastapi import APIRouter

from ..dependencies.client_session_dependencies import ClientSessionDependency
from ..dependencies.models_dependencies import (
    SearchAlertDependency,
    SearchAlertsDependency,
)
from ..dependencies.services_dependencies import ORMSessionDependency
from ..models.search_alert_model import (
    SearchAlert,
    SearchAlertCreate,
    SearchAlertPublic,
)

router = APIRouter(
    prefix='/search-alerts',
    tags=['search alerts'],
    responses={404: {'description': 'Search Alert not found'}},
)


@router.get('/', response_model=list[SearchAlertPublic])
async def find_search_alerts(search_alerts: SearchAlertsDependency):
    return search_alerts


@router.post('/')
async def create_search_alert(
    search_alert: SearchAlertCreate,
    client_session: ClientSessionDependency,
    orm_session: ORMSessionDependency,
):
    db_search_alert = SearchAlert.model_validate(
        search_alert, update={'user_id': client_session.id}
    )
    orm_session.add(db_search_alert)
    orm_session.commit()
    orm_session.refresh(db_search_alert)
    return db_search_alert


@router.get('/{search_alert_id}', response_model=SearchAlertPublic)
async def read_search_alert(search_alert: SearchAlertDependency):
    return search_alert


@router.delete('/{search_alert_id}', status_code=204)
async def delete_search_alert(
    search_alert: SearchAlertDependency, orm_session: ORMSessionDependency
):
    orm_session.delete(search_alert)
    orm_session.commit()
