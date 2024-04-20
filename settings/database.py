from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

env = dotenv_values(".env")

DB_URL = env.get("DB_URL")

engine = create_async_engine(DB_URL, echo=True, future=True)

Session = async_sessionmaker(bind=engine)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
