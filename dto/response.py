import json
from typing import Generic, TypeVar

import strawberry
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate

TData = TypeVar("TData")


@strawberry.type
class ResponseObject:
    id: int
    code: int
    status: bool
    message: str

    @classmethod
    def get_response(cls, response_id: int, custom_message: str | None = None):
        with open("assets/response_codes.json") as file:
            response_data = json.load(file)

        matching_response = next(
            (response for response in response_data if response["id"] == response_id), None
        )
        if matching_response:
            code = matching_response.get("code", "")
            message = custom_message if custom_message else matching_response["message"]
            status = matching_response["status"]
            return cls(id=response_id, code=code, status=status, message=message)

        return cls(id=-1, code=0000, status=False, message="Invalid response ID")


@strawberry.type
class PageObject:
    number: int
    per_page: int
    current_page: int
    last_page: int
    has_nex_page: bool

    def __init__(
        self, number: int, per_page: int, current_page: int, last_page: int, has_nex_page: bool
    ):
        self.number = number
        self.per_page = per_page
        self.current_page = current_page
        self.last_page = last_page
        self.has_nex_page = has_nex_page

    @classmethod
    def get_page(cls, page_obj: "PageObject"):
        return cls(
            number=page_obj.number,
            per_page=page_obj.per_page,
            current_page=page_obj.current_page,
            last_page=page_obj.last_page,
            has_more_pages=page_obj.has_more_pages,
        )


@strawberry.type
class Response(Generic[TData]):
    response: ResponseObject
    data: TData | None

    def __init__(self, response: ResponseObject, data: TData | None = None):
        self.response = response
        self.data = data

    @classmethod
    def get_response(
        cls,
        response_id: int,
        custom_message: str | None = None,
        data: TData | None = None,
    ) -> "Response[TData]":
        response = ResponseObject.get_response(response_id, custom_message)
        return cls(response=response, data=data)
