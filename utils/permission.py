import typing

import strawberry
from strawberry.permission import BasePermission

from dto.response import Response
from utils.auth import get_current_user


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        user = await get_current_user(info)
        if user:
            return True
        return False

    def on_unauthorized(self):
        return Response.get_response(response_id=0)


class IsAdmin(BasePermission):
    message = "User is not admin"

    async def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        user = await get_current_user(info)
        if user and user.is_admin:
            return True
        return False

    def on_unauthorized(self):
        return Response.get_response(response_id=0)


class IsAuthorized(BasePermission):
    permissions: list[str] | None = None

    def __init__(self, permissions: list[str] | None = None, *args, **kwargs):
        self.permissions = permissions
        super().__init__(*args, **kwargs)

    message = "User is not authorized"

    async def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        user = await get_current_user(info)
        if not user:
            return False

        user_permissions = [
            "can_create_user",
            "can_view_user",
            "can_update_user",
            "can_delete_user",
        ]  # TODO: get permissions from user
        if self.permissions and not any(
            permission in user_permissions for permission in self.permissions
        ):
            return False

        return True

    def on_unauthorized(self):
        return Response.get_response(response_id=0, custom_message="User is not authorized")
