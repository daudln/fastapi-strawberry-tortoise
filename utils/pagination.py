from typing import Any, Callable

from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from strawberry.types import Info
from tortoise.expressions import Q
from tortoise.models import Model

from dto.response import ResponseObject


async def get_paginated_data(
    model: Model,
    filters: Q,
    builder_function: Callable[[str], Any],
    page_number: int,
    items_per_page: int = None,
    lookup: str = "unique_id",
    info: Info = None,
) -> tuple[ResponseObject, Page, list[Any]]:
    """
    Fetches, paginates, and builds data for a given model class.

    Args:
        model (Model): The Tortoise model to query.
        filters (Q): The filters to apply to the queryset.
        page_number (int): The desired page number.
        builder_function (function): A function that takes a model object's lookup(str) and returns its data.
        items_per_page (int): Number of items per page, default is 20.
        lookup (str): The field to select in the queryset.

    Returns:
        tuple: A tuple containing the response, page, data.
    """

    queryset = await model.filter(filters).distinct().only(lookup)
    paginated_data = await paginate(queryset, params={"limit": items_per_page})
    page_obj = paginated_data.page(page_number)
    data = [builder_function(getattr(obj, lookup)) for obj in page_obj]
    page = Page.page(paginated_data.page(page_number))
    return ResponseObject.get_response(id=1), page, data
    # page_obj = paginated_data.page(page_number)
    # data = [builder_function(getattr(obj, lookup)) for obj in page_obj]
    # page = Page.page(paginated_data.page(page_number))
    # return await info.return_type(response=ResponseObject.get_response(id=1), page=page, data=data)
