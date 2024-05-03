from typing import Type

from tortoise import fields
from tortoise.signals import post_save

from mixins.models import BaseModel


class User(BaseModel):
    name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200)
    password = fields.CharField(max_length=200)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        table = "users"


@post_save(User)
async def send_welcome_message_for_new_user(
    sender: "Type[User]", instance: User, created: bool, using_db: bool, update_fields: list
) -> None: ...


class Profile(BaseModel):
    first_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    address = fields.CharField(max_length=200)
    phone_number = fields.CharField(max_length=200)
    user = fields.OneToOneField("models.User", related_name="profile", on_delete=fields.CASCADE)
