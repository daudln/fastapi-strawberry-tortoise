from typing import Type

from tortoise.signals import post_save

from core.models import User
from utils.mail import send_mail


@post_save(User)
async def send_welcome_message_for_new_user(
    sender: "Type[User]", instance: User, created: bool, **kwargs: dict
):
    if created:
        await send_mail(
            to=[instance.email],
            body={"name": instance.name},
            subject="Welcome to Task Manager",
            template_name="emails/welcome.html",
        )
