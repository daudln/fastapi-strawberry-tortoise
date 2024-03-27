from fastapi import APIRouter

core_routes = APIRouter(prefix="/core", tags=["Core"])


@core_routes.get("/")
async def health() -> dict[str, str]:
    return {"status": "Core is up and running"}


@core_routes.put("/users/{user_id}")
async def update_user(user_id: int):
    pass


@core_routes.delete("/users/{user_id}")
async def delete_user(user_id: int):
    pass
