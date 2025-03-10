from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult
from core.models import UserToken


class VerifToken:

    @staticmethod
    async def get_verif_token_user(
        session: AsyncSession, verif_token: str
    ) -> UserToken | None:
        stmt = select(UserToken).where(UserToken.token == verif_token)
        user_token: ScalarResult[UserToken] = await session.scalars(stmt)
        return user_token.one_or_none()

    @staticmethod
    async def delete_user_verif_token(session: AsyncSession, token_id: int) -> bool:
        stmt = select(UserToken).where(UserToken.id == token_id)
        token_scalar = await session.scalars(stmt)
        token_data = token_scalar.one_or_none()
        if token_data:
            await session.delete(token_data)
            await session.commit()
            return True
        else:
            return False
