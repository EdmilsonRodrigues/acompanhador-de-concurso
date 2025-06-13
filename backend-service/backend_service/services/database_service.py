from functools import cache

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from ..config import Settings


@cache
def get_engine() -> Engine:  # pragma: no cover
    """
    Returns a connection to the database. The connection is cached,
        so it is only created once.

    :return: A connection to the database
    :rtype: sqlalchemy.Engine
    """
    connect_args = {'check_same_thread': False}
    return create_engine(Settings().DATABASE_URL, connect_args=connect_args)


def create_db_and_tables(engine: Engine) -> None:  # pragma: no cover
    """
    Creates the database and tables

    :param engine: A connection to the database
    :type engine: sqlalchemy.Engine

    :return: None
    :rtype: None
    """
    SQLModel.metadata.create_all(engine)
