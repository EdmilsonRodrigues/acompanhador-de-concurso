import base64
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated, Any

import bcrypt
import jwt
import oci
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from ..config import Environment, Settings
from ..exceptions.services_exceptions import (
    InvalidTokenException,
    UnmatchedPasswordException,
)
from ..services.logging_service import get_logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]
logger = get_logger()


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


def hash_password(password: str) -> str:
    """
    Hashes a password

    :param password: the password to hash
    :type password: str

    :return: the hashed password
    :rtype: str
    """
    password_bytes = password.encode('utf-8')

    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed_password: str) -> None:
    """
    Checks if a password matches a hashed password

    :param password: the password to check
    :type password: str
    :param hashed_password: the hashed password to check against
    :type hashed_password: str

    :raises UnmatchedPasswordException: if the password does not match the
        hashed password

    :returns: None
    :rtype: None
    """
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    try:
        if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
            raise UnmatchedPasswordException
    except Exception as exc:
        logger.error({
            'msg': 'Error checking password',
            'password': password,
            'hashed_password': hashed_password,
            'error': str(exc),
        })
        raise exc


def _get_rsa_private_key() -> bytes:  # pragma: no cover
    settings = Settings()
    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        logger.info('Loading private key from file')
        with Path(settings.RSA_PRIVATE_KEY).open(mode='rb') as f:
            return f.read()

    logger.info('Loading private key from OCI secret')
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    secrets_client = oci.secrets.SecretsClient(config={}, signer=signer)

    try:
        get_secret_bundle_response = secrets_client.get_secret_bundle(
            settings.RSA_PRIVATE_KEY
        )
        secret_bundle = get_secret_bundle_response.data
        base64_secret_content = secret_bundle.secret_bundle_content.content
        decoded_secret_content = base64.b64decode(base64_secret_content)

        return decoded_secret_content
    except Exception as exc:
        logger.error('Error fetching secret', exc)
        raise exc


def _load_private_key_from_pem_bytes(
    private_key_bytes: bytes,
) -> rsa.RSAPrivateKey:
    return serialization.load_pem_private_key(
        private_key_bytes,
        password=Settings().PEM_PASSWORD_BYTES,
        backend=default_backend(),
    )


RSA_PRIVATE_KEY = _load_private_key_from_pem_bytes(_get_rsa_private_key())
RSA_PUBLIC_KEY = RSA_PRIVATE_KEY.public_key()


logger.info('Loaded private key')
logger.info('Generated public key')


def generate_auth_token(user_id: int) -> str:
    """
    Generates an auth token

    :param user_id: the user id
    :type user_id: int

    :return: the auth token
    :rtype: str
    """
    return _generate_jwt_token(
        user_id,
        datetime.now(UTC) + timedelta(seconds=Settings().EXPIRATION_TIME),
    )


def generate_refresh_token(user_id: int) -> str:
    """
    Generates a refresh token

    :param user_id: the user id
    :type user_id: int

    :return: the refresh token
    :rtype: str
    """
    return _generate_jwt_token(
        user_id,
        datetime.now(UTC)
        + timedelta(seconds=Settings().REFRESH_TOKEN_EXPIRATION_TIME),
    )


def decode_jwt_token(token: str) -> int:
    """
    Decodes a JWT token and returns the user id

    :param token: the JWT token to decode
    :type token: str

    :return: the user id
    :rtype: int
    """
    user_id = _decode_jwt_token(token)['sub']

    return int(user_id)


def _generate_jwt_token(subject: Any, expiration_time: int) -> str:
    token = jwt.encode(
        {
            'sub': str(subject),
            'exp': expiration_time,
            'iat': datetime.now(UTC),
        },
        RSA_PRIVATE_KEY,
        algorithm='RS256',
    )

    return token


def _decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, RSA_PUBLIC_KEY, algorithms=['RS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as exc:
        logger.debug({
            'msg': 'Error decoding JWT token',
            'token': token,
            'error': str(exc),
        })
        raise InvalidTokenException from exc
    except Exception as exc:  # pragma: no cover
        logger.error({
            'msg': 'Error decoding JWT token',
            'token': token,
            'error': str(exc),
        })
        raise exc
    return payload
