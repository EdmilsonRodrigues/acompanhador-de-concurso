import os
from enum import Enum
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .services.logging_service import get_logger

VERSION = '1.0.0'

logger = get_logger()


class Environment(Enum):
    TESTING = 'Testing'
    DEVELOPMENT = 'Development'
    PRODUCTION = 'Production'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_ignore_empty=True, extra='ignore'
    )

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DATABASE_URL: str = 'sqlite:///:memory:'
    API_URL: str = 'http://localhost:8000'
    FRONTEND_URL: str = 'http://localhost:4200'

    SECRET_KEY: str = os.urandom(32).hex()
    EXPIRATION_TIME: int = 60 * 60
    REFRESH_TOKEN_EXPIRATION_TIME: int = 60 * 60 * 24 * 7

    RSA_PRIVATE_KEY: Annotated[str, Field()]
    PEM_PASSWORD_BYTES: Annotated[bytes, Field()]


class StripeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        env_prefix='STRIPE_',
        extra='ignore',
    )

    PUBLIC_KEY: Annotated[str, Field()]
    SECRET_KEY: Annotated[str, Field()]
    WEBHOOK_SECRET: Annotated[str, Field()]


logger.info({'version': VERSION, 'environment': Environment.DEVELOPMENT.value})
