import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict

from .services.logging_service import get_logger

VERSION = '1.0.0'

logger = get_logger()


class Environment(Enum):
    DEVELOPMENT = 'Development'
    PRODUCTION = 'Production'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True)

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DATABASE_URL: str = 'sqlite:///:memory:'

    SECRET_KEY: str = os.urandom(32).hex()
    EXPIRATION_TIME: int = 60 * 60
    REFRESH_TOKEN_EXPIRATION_TIME: int = 60 * 60 * 24 * 7

    RSA_PRIVATE_KEY: str
    PEM_PASSWORD_BYTES: bytes
    SECRET_OCID: str


logger.info({'version': VERSION, 'environment': Environment.DEVELOPMENT.value})
