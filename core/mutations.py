import strawberry
from strawberry.types import Info

from builder.core import CoreBuider
from core.models import User
from dto.core import LoginInput, TokenObject, UserInput, UserObject
from dto.response import Response
from utils.auth import get_password_hash, login_for_access_token
from utils.validators import validate_email, validate_password


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user_mutation(self, info:Info,  input: UserInput) -> Response[UserObject]:
        if not validate_email(input.email):
            return Response.get_response(response_id=2)
        
        if not validate_password(input.password):
            return Response.get_response(response_id=4)
        
        if input.password != input.password_confirm:
            return Response.get_response(response_id=3)
        
        if await User.filter(name=input.name, email=input.email).exists():
            return Response.get_response(response_id=5)
        
        hashed_password = get_password_hash(input.password)
        user = await User.create(name=input.name, email=input.email, password=hashed_password)
        return Response.get_response(response_id=1, data=CoreBuider.get_user_data(user.unique_id))
    
    @strawberry.mutation
    async def login_mutation(self, info:Info, input: LoginInput) -> Response[TokenObject]:
        token = await login_for_access_token(input.username, input.password)
        if token:
            return Response.get_response(response_id=1, data=token)
        
        return Response.get_response(response_id=9)