from typing import Annotated

from sqlmodel import Field, SQLModel


class SearchAlertBase(SQLModel):
    area: Annotated[
        str,
        Field(description='The area of the job, like Professor or Policial'),
    ]
    state: Annotated[
        str, Field(description='The state of the job, like SP or RJ')
    ]


class SearchAlert(SearchAlertBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    user_id: Annotated[int, Field(foreign_key='user.id', index=True)]


class SearchAlertPublic(SearchAlertBase):
    id: Annotated[int, Field()]


class SearchAlertCreate(SearchAlertBase): ...
