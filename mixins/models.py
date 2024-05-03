import uuid
from datetime import datetime
from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

primary_key = Annotated[int, mapped_column(primary_key=True, index=True, unique=True)]
created_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]
updated_at = Annotated[
    datetime,
    mapped_column(nullable=False, default=datetime.now(), server_default=func.CURRENT_TIMESTAMP()),
]
unique_id = Annotated[uuid.UUID, mapped_column(nullable=False, default=uuid.uuid4, unique=True)]
is_active = Annotated[bool, mapped_column(nullable=False, default=True)]


class BaseModel(DeclarativeBase):
    id: Mapped[primary_key]
    unique_id: Mapped[unique_id]
    is_active: Mapped[is_active]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
