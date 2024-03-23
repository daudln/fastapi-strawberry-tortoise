from tortoise import fields

from mixins.models import BaseModel
from tortoise.signals import post_save

from utils.mail import send_mail
from typing import Type


class User(BaseModel):
    name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200)
    password = fields.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        table = "users"


@post_save(User)
async def send_welcome_message_for_new_user(
    sender: "Type[User]", instance: User, created: bool, using_db, update_fields
):
    if created:
        await send_mail(
            to=[instance.email],
            body={"name": instance.name},
            subject="Welcome to Task Manager",
            template_name="emails/welcome.html",
        )


class Profile(BaseModel):
    first_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    address = fields.CharField(max_length=200)
    phone_number = fields.CharField(max_length=200)
    user = fields.OneToOneField("models.User", related_name="profile")
