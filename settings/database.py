from dotenv import dotenv_values

CONF = dotenv_values(".env")

DB_URL = CONF.get("DB_URL")

ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": [
                "aerich",
                "core.models",
            ]
        }
    },
}
