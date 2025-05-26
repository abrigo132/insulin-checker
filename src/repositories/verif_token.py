from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult
from typing import Type

from core.models import UserToken


class VerifTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.model: Type[UserToken] = UserToken

    async def get_verif_token_user(
        self,
        verif_token: str,
    ) -> UserToken | None:
        stmt = select(self.model).where(self.model.token == verif_token)
        user_token: ScalarResult[UserToken] = await self.session.scalars(stmt)
        return user_token.one_or_none()

    async def delete_user_verif_token(
        self,
        token_id: int,
    ) -> bool:
        stmt = select(self.model).where(self.model.id == token_id)
        token_scalar = await self.session.scalars(stmt)
        token_data = token_scalar.one_or_none()
        if token_data:
            await self.session.delete(token_data)
            await self.session.flush()
            return True
        else:
            return False

    async def add_user_token(
        self,
        user_id: int,
        token: str,
    ) -> UserToken:
        user_token: UserToken = UserToken(token=token, user_id=user_id)
        self.session.add(user_token)
        await self.session.flush()
        return user_token
