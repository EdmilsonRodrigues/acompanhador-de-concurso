from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..services.database_service import get_engine


def _get_orm_session():  # pragma: no cover
    with Session(get_engine()) as session:
        yield session


ORMSessionDependency = Annotated[Session, Depends(_get_orm_session)]
