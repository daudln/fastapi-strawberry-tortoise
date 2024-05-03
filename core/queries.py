import strawberry
from fastapi_pagination.ext.tortoise import paginate
from strawberry.types import Info

from builder.core import CoreBuider
from core.models import User
from dto.core import UserObject
from dto.response import Response
from utils.auth import get_current_user


@strawberry.type
class Query:
    @strawberry.field
    async def hello(self, info: Info, name: str | None = None) -> str:
        return f"Hello {name or 'world'}"

    @strawberry.field
    async def get_users(self, info: Info) -> Response[list[UserObject]]:
        users = User.all()
        return Response.get_response(
            response_id=1,
            data=users,
        )

    @strawberry.field
    async def get_user(self, info: Info) -> Response[UserObject]:
        user = await get_current_user(info)
        if not user:
            return Response.get_response(response_id=10)

        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))

    @strawberry.field
    async def get_me(self, info: Info) -> Response[UserObject]:
        user = await get_current_user(info)
        if not user:
            return Response.get_response(response_id=10)

        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))
