import strawberry


@strawberry.interface
class GenericFilterInput:
    page_number: int = strawberry.field(default_value=1)
    items_per_page: int = strawberry.field(default_value=20)
