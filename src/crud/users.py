from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult

from core.schemas import UserCreate
from core.models import User, UserToken
from core.auth.register import hashed_password


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

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User:
        stmt = select(User).where(User.username == username)
        user_result: ScalarResult[User] = await session.scalars(stmt)
        return user_result.one_or_none()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        user_result: ScalarResult[User] = await session.scalars(stmt)
        return user_result.one_or_none()
