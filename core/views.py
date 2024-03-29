from typing import Any, Dict, List, Sequence

from starlette.requests import Request
from starlette_admin import BaseModelView, IntegerField, StringField, TagsField


class UserView(BaseModelView):
    pk_attr = "id"

    fields = [
        IntegerField("id"),
        IntegerField("name"),
        StringField("email"),
        TagsField("is_active"),
    ]

    async def count(self, request: Request):
        return await self.model.all().count()


class ProfileView(BaseModelView):
    pk_attr = "id"
    identity = "profile"
    name = "Profile"
    label = "User Profile"
    icon = "fa-regular fa-user"
    list_display = ("first_name", "last_name", "address", "phone_number")
    search_fields = ("first_name", "last_name", "address", "phone_number")
    filter_fields = ("first_name", "last_name", "address", "phone_number")
    sortable_fields = ("first_name", "last_name", "address", "phone_number")

    fields = [
        IntegerField("id"),
        IntegerField("first_name"),
        IntegerField("last_name"),
        IntegerField("address"),
        IntegerField("phone_number"),
    ]

    async def count(self, request: Request):
        return await self.model.all().count()

    async def find_all(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        where: Dict[str, Any] | str | None = None,
        order_by: List[str] | None = None,
    ) -> Sequence[Any]:
        return await super().find_all(request, skip, limit, where, order_by)

    async def find_one(self, request: Request, pk: int) -> Any:
        return await super().find_one(request, pk)
