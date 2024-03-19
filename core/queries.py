import strawberry
from strawberry.types import Info

@strawberry.type
class Query:
    @strawberry.field
    def hello(self, info:Info, name: str|None = None) -> str:
        return f"Hello {name or 'world'}"