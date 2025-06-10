from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..services.database_service import get_engine


def get_orm_session():
    with Session(get_engine()) as session:
        yield session


ORMSessionDependency = Annotated[Session, Depends(get_orm_session)]
