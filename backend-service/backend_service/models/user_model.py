from typing import Annotated

from pydantic import BeforeValidator, EmailStr
from sqlmodel import Field, SQLModel

from ..services.auth_service import hash_password

HashedPassword = Annotated[str, BeforeValidator(hash_password)]


class UserBase(SQLModel):
    name: Annotated[str, Field()]
    email: Annotated[EmailStr, Field(unique=True, index=True)]


class User(UserBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    password: str

    is_admin: bool = False
    is_active: bool = True

    def deactivate(self):
        self.is_active = False


class UserPublic(UserBase):
    id: Annotated[int, Field()]


class UserCreate(UserBase):
    password: Annotated[HashedPassword, Field()]


class UserUpdate(UserBase):
    name: Annotated[str | None, Field()] = None
    email: Annotated[str | None, Field()] = None
    password: Annotated[str | None, Field()] = None
