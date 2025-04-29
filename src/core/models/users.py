from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
import datetime
from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    sensitivity: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)


class UserToken(Base):
    token: Mapped[str] = mapped_column(unique=True, nullable=True, index=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now() + datetime.timedelta(days=2)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
