from tortoise import fields

from mixins.models import BaseModel

class User(BaseModel):
    name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200)
    password = fields.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        table = 'users'
    
    
class Profile(BaseModel):
    first_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    address = fields.CharField(max_length=200)
    phone_number = fields.CharField(max_length=200)
    user = fields.OneToOneField('models.User', related_name='profile')