from functools import singledispatchmethod
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, EmailStr
from sqlmodel import Field, SQLModel

from ..exceptions.services_exceptions import UnmatchedPasswordException
from ..services.auth_service import check_password, hash_password

HashedPassword = Annotated[str, BeforeValidator(hash_password)]


class UserBase(SQLModel):
    name: Annotated[str, Field()]
    email: Annotated[EmailStr, Field(unique=True, index=True)]


class UserUpdate(BaseModel):
    name: Annotated[str | None, Field()] = None
    email: Annotated[EmailStr | None, Field()] = None


class UserPasswordUpdate(BaseModel):
    old_password: Annotated[str, Field()]
    new_password: Annotated[HashedPassword, Field()]


class User(UserBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    password: str

    is_admin: bool = False
    is_active: bool = True

    def deactivate(self):
        self.is_active = False

    @singledispatchmethod
    def update(self, updated_data): ...

    @update.register
    def _(self, updated_data: UserUpdate):
        user_data = updated_data.model_dump(exclude_unset=True)
        self.sqlmodel_update(user_data)

    @update.register
    def _(self, updated_data: UserPasswordUpdate):
        check_password(updated_data.old_password, self.password)
        if self.password == updated_data.new_password:
            raise UnmatchedPasswordException(
                'New password is the same as the old one'
            )
        self.password = updated_data.new_password


class UserPublic(UserBase):
    id: Annotated[int, Field()]


class UserCreate(UserBase):
    password: Annotated[HashedPassword, Field()]
