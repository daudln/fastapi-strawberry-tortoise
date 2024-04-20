import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mixins.models import BaseModel


class ProfileType(enum.Enum):
    ADMIN = "Admin"
    NORMAL_USER = "Normal User"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)

    def __repr__(self) -> str:
        return self.name


class Profile(BaseModel):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    phone_number: Mapped[str] = mapped_column(String(12), nullable=True)
    profile_type: Mapped[ProfileType] = mapped_column(default=ProfileType.NORMAL_USER)
    user_id = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)
