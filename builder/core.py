from core.models import User
from dto.core import UserObject


class CoreBuider:
    @staticmethod
    async def get_user_data(unique_id:str)->UserObject | None:
        user = await User.get(unique_id=unique_id)
        if user:
            return UserObject(unique_id=user.unique_id, name=user.name, email=user.email)
        return None