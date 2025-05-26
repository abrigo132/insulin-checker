from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult
from typing import Type

from core.schemas import UserCreate
from core.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.model: Type[User] = User

    async def add(
        self,
        user_create: UserCreate,
    ) -> User:
        user: User = self.model(
            **user_create.model_dump(),
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_username(
        self,
        username: str,
    ) -> User:
        stmt = select(self.model).where(self.model.username == username)
        user_result: ScalarResult[User] = await self.session.scalars(stmt)
        return user_result.one_or_none()

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User:
        stmt = select(self.model).where(self.model.id == user_id)
        user_result: ScalarResult[User] = await self.session.scalars(stmt)
        return user_result.one_or_none()

    async def change_flag_is_verified(
        self,
        user_id: int,
    ) -> User | bool:
        stmt = select(self.model).where(self.model.id == user_id)
        user_scalar: ScalarResult[User] = await self.session.scalars(stmt)
        user_info = user_scalar.one_or_none()

        if user_info:
            user_info.is_verified = True
            await self.session.flush()
            await self.session.refresh(user_info)
            return user_info
        else:
            return False
