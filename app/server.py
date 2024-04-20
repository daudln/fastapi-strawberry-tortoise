from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings.database import Session

from .main_schema import graphql_app

CONF = dotenv_values(".env")

DEBUG = CONF.get("DEBUG", "False") == "True"


async def lifespan(app: FastAPI):
    db = Session()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(debug=DEBUG, lifespan=lifespan)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/api")
