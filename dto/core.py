from uuid import UUID

import strawberry
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from core.models import User
from dto.response import ResponseObject
from utils.auth import Token


class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_confirm: str


@strawberry.input
class UserInput:
    name: str
    email: str
    password: str
    password_confirm: str


GetUser = pydantic_model_creator(User, name="UserGet", exclude=("password", "password_confirm"))


@strawberry.type
class UserObject:
    unique_id: UUID
    name: str
    email: str


@strawberry.type
class UserResponseObject:
    response: ResponseObject
    data: UserObject | None = None


@strawberry.input
class LoginInput:
    username: str
    password: str


@strawberry.experimental.pydantic.type(model=Token, all_fields=True)
class TokenObject:
    response: ResponseObject
