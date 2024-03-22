from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import register_tortoise

from settings.database import ORM

from .main_schema import graphql_app

CONF = dotenv_values(".env")

DEBUG = CONF.get("DEBUG", "False") == "True"

app = FastAPI(debug=DEBUG)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/api")

register_tortoise(
    app,
    config=ORM,
    add_exception_handlers=True,
    generate_schemas=False if DEBUG else True,
)

add_pagination(app)
