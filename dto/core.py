from uuid import UUID
import strawberry
from strawberry.field import StrawberryField as Field
from strawberry.experimental import pydantic
from pydantic import EmailStr, BaseModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from core.models import User
from dto.response import ResponseObject



class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    

# @pydantic.input(model=UserModel, all_fields=True)
# class UserInput:
#     pass
    
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
