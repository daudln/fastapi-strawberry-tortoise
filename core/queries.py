import strawberry
from strawberry.types import Info

from builder.core import CoreBuider
from core.models import User
from dto.core import UserObject
from dto.response import PageObject, Response
from utils.auth import get_current_user
from utils.paginator import Paginator
from tortoise.expressions import Q

@strawberry.type
class Query:
    @strawberry.field
    async def hello(self, info:Info, name: str|None = None) -> str:
        return f"Hello {name or 'world'}"
    
    @strawberry.field
    async def get_users(self, info:Info) -> Response[list[UserObject]]:
        users = User.all()
        paginator = Paginator(users, 1)
        page = await paginator.get_page(2)
        data = [await CoreBuider.get_user_data(obj.unique_id) for obj in page]
        return Response.get_response(response_id=1, page=PageObject(number=page.number, per_page=page.paginator.per_page, current_page=page.number, last_page=page.has_previous, has_nex_page=False), data=users)
    
    
    @strawberry.field
    async def get_user(self, info:Info) -> Response[UserObject]:
        user = await get_current_user(info)
        if not user:
            return Response.get_response(response_id=10)
        
        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))
    
    @strawberry.field
    async def hello(self, info:Info, name: str|None = None) -> str:
        return f"Hello {name or 'world'}"
    
    @strawberry.field
    async def get_me(self, info:Info) -> Response[UserObject]:
        user = await get_current_user(info)
        if not user:
            return Response.get_response(response_id=10)
        
        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))