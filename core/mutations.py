import strawberry
from strawberry.types import Info

from builder.core import CoreBuider
from core.models import User
from dto.core import UserInput, UserObject
from dto.response import Response

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user_mutation(self, info:Info,  input: UserInput) -> Response[UserObject]:
        if input.password != input.password_confirm:
            return Response.get_response(response_id=2)
        
        if await User.filter(email=input.email).exists():
            return Response.get_response(response_id=3)
        
        if await User.filter(name=input.name).exists():
            return Response.get_response(response_id=4)
        
        user = await User.create(name=input.name, email=input.email, password=input.password)
        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))