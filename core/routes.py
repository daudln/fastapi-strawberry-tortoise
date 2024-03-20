from fastapi import APIRouter

from dto.core import GetUser, User, UserModel

core_routes = APIRouter(prefix="/core", tags=["Core"]
)

@core_routes.get("/")
async def health():
    return {"status": "Core is up and running"}

@core_routes.post("/users")
async def create_user(input: UserModel):
    user = await User.create(**input.model_dump())
    return GetUser.from_queryset_single(User.get(id=user.id))

@core_routes.get("/users")
async def get_users():
    users = await GetUser.from_queryset(User.all())
    return users

@core_routes.get("/users/{user_id}")
async def get_user(user_id: int):
    user = GetUser.from_queryset_single(User.filter(id=user_id).first())
    return user

@core_routes.put("/users/{user_id}")
async def update_user(user_id: int):
    pass

@core_routes.delete("/users/{user_id}")
async def delete_user(user_id: int):
    pass