from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

CONF = dotenv_values(".env")


class EmailSchema(BaseModel):
    email: list[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=CONF.get("MAIL_USERNAME"),
    MAIL_PASSWORD=CONF.get("MAIL_PASSWORD"),
    MAIL_FROM=CONF.get("MAIL_FROM"),
    MAIL_PORT=CONF.get("MAIL_PORT"),
    MAIL_SERVER=CONF.get("MAIL_SERVER"),
    MAIL_FROM_NAME=CONF.get("MAIL_FROM_NAME"),
    MAIL_STARTTLS=CONF.get("MAIL_STARTTLS"),
    MAIL_SSL_TLS=CONF.get("MAIL_SSL_TLS"),
    USE_CREDENTIALS=CONF.get("USE_CREDENTIALS")=="True",
    VALIDATE_CERTS=CONF.get("VALIDATE_CERTS")=="True",
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates/",
)


async def send_mail(
    to: list[EmailSchema], body: dict[str, Any], subject: str, template_name: str
) -> JSONResponse:
    message = MessageSchema(
        subject=subject,
        recipients=to,
        subtype=MessageType.html,
        template_body=body,
    )

    body.update({"year": datetime.now().year})

    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
