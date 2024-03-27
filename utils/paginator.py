import math
from collections.abc import Sequence

from tortoise.queryset import QuerySet


class UnorderedObjectListWarning(RuntimeWarning):
    pass


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator:
    default_error_messages = {
        "invalid_page": "Invalid page (%(page_number)s)",
        "min_page": "That page number is less than 1",
        "no_results": "That page contains no results",
    }

    def __init__(
        self,
        queryset: QuerySet,
        per_page: int,
        orphans: int = 0,
        allow_empty_first_page: bool = True,
        error_messages: str | None = None,
    ):
        self.queryset = queryset
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page
        self.error_messages = (
            self.default_error_messages
            if error_messages is None
            else self.default_error_messages | error_messages
        )

    async def validate_number(self, number: int):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(self.error_messages["invalid_page"])
        if number < 1:
            raise EmptyPage(self.error_messages["min_page"])
        if number > await self.num_pages():
            raise EmptyPage(self.error_messages["no_results"])
        return number

    async def num_pages(self):
        """
        Calculate the total number of pages based on the total count and per-page value.
        """
        count = await self.count
        if count is None:
            raise ValueError("Paginator must have a `count` attribute set")
        return math.ceil(count / self.per_page)

    async def page(self, number: int):
        number = await self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        return self._get_page(self.queryset[bottom:top], number, self)

    async def get_page(self, number: int):
        number = await self.validate_number(number)
        offset = (number - 1) * self.per_page
        limited = self.queryset.limit(self.per_page).offset(offset)
        return self._get_page(limited, number, self)

    def _get_page(self, *args, **kwargs):
        # TODO: ... implement logic for creating a Page object (optional)
        return Page(*args, **kwargs)  # Assuming a separate Page class definition

    @property
    async def count(self) -> int:
        return await self.queryset.count()

    # TODO: ... implement other methods like `num_pages`, `page_range`, etc. (optional)


class Page(Sequence):
    def __init__(self, object_list: list, number: int = 1, paginator: Paginator = None):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return "<Page %d of %s>" % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index: int):
        # TODO: ... implement logic for item access (optional)
        return self.object_list[index]

    @property
    def has_next(self):
        return self.number < self.paginator.num_pages

    @property
    def has_previous(self):
        return self.number > 1

    def next_page_number(self):
        if self.has_next:
            return self.number + 1
        return None

    def previous_page_number(self):
        if self.has_previous:
            return self.number - 1
        return None

    def start_index(self):
        return (self.number - 1) * self.paginator.per_page + 1

    def end_index(self):
        return self.number * self.paginator.per_page

    def as_dict(self):
        return self.object_list.as_dict(exclude=None)
