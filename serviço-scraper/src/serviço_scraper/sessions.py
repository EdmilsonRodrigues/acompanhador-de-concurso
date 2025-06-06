from functools import cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base

from .config import Config


@cache
def get_motor() -> Engine:
    return create_engine(Config.DB_URL)


Base = declarative_base()
