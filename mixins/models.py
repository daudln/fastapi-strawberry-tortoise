import uuid

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.IntField(pk=True)
    unique_id = fields.UUIDField(default=uuid.uuid4)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseOneToOneModel(Model):
    unique_id = fields.UUIDField(default=uuid.uuid4)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class NameMixin:
    name = fields.CharField(max_length=255)
