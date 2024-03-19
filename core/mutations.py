import strawberry
from strawberry.types import Info

from builder.core import CoreBuider
from core.models import User
from dto.core import UserInput, UserResponseObject
from dto.response import ResponseObject

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user_mutation(self, info:Info,  input: UserInput) -> UserResponseObject:
        if input.password != input.password_confirm:
            return UserResponseObject(response=ResponseObject.get_response(2))
        
        if await User.filter(email=input.email).exists():
            return UserResponseObject(response=ResponseObject.get_response(3))
        
        if await User.filter(name=input.name).exists():
            return UserResponseObject(response=ResponseObject.get_response(4))
        
        user = await User.create(name=input.name, email=input.email, password=input.password)
        return UserResponseObject(response=ResponseObject.get_response(1), data=CoreBuider.get_user_data(user.unique_id))
