from typing import Annotated

from fastapi import Depends

from settings.database import Session


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
