from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.users import UserCreate
from src.core.models.users import User
from src.core.auth.register.utils import hashed_password


class UsersCrud:

    @staticmethod
    async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
        user_data = user_create.model_dump(exclude={"password", "confirm_password"})
        user: User = User(
            **user_data, hashed_password=hashed_password(password=user_create.password)
        )
        session.add(user)
        await session.commit()
        return user
