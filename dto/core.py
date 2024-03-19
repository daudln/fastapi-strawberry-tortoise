import strawberry

from dto.response import ResponseObject


@strawberry.input
class UserInput:
    name: str
    email: str
    password: str
    password_confirm: str


@strawberry.type
class UserObject:
    unique_id: str
    name: str
    email: str


@strawberry.type
class UserResponseObject:
    response: ResponseObject
    data: UserObject | None = None
