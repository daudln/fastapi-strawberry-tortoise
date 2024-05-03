from tortoise import fields
from tortoise.fields import CASCADE

from mixins.models import BaseOneToOneModel


class AccountActivationToken(BaseOneToOneModel):
    is_used = fields.BooleanField(default=False)
    user = fields.OneToOneField(
        "models.User", on_delete=CASCADE, pk=True, related_name="activation_token"
    )

    class Meta:
        table = "account_activation_token"
