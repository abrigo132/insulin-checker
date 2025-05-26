import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth.login import create_access_jwt, create_refresh_jwt
from core.auth.register import (
    create_confirm_register_token_url,
    check_confirm_password_with_password,
    hashed_password,
    check_hash_password,
)
from core.models import db_helper, User, UserToken
from repositories import UserRepository, VerifTokenRepository
from core.schemas import UserRegisterCreds, UserCreate, UserLogin, TokenInfo
from tasks import send_verification_message


class UserService:
    def __init__(self, session: AsyncSession = Depends(db_helper.session_getter)):
        self.session: AsyncSession = session
        self.user_repo: UserRepository = UserRepository(session=session)
        self.verif_token_repo: VerifTokenRepository = VerifTokenRepository(
            session=session
        )

    async def create_user(self, user_creds: UserRegisterCreds) -> User:
        if not await check_confirm_password_with_password(
            password=user_creds.password,
            confirm_password=user_creds.confirm_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают"
            )
        new_user: User = await self.user_repo.add(
            user_create=UserCreate(
                username=user_creds.username,
                email=user_creds.email,
                weight=user_creds.weight,
                hashed_password=hashed_password(user_creds.password),
            )
        )
        verif_token: str = create_confirm_register_token_url()
        verif_token_for_user: UserToken = await self.verif_token_repo.add_user_token(
            user_id=new_user.id, token=verif_token
        )
        await send_verification_message.kiq(new_user.id, verif_token_for_user.token)
        await self.session.commit()
        return new_user

    async def login_user(
        self, user_creds_login: UserLogin
    ) -> TokenInfo | HTTPException:
        invalid_credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
        user: User | None = await self.user_repo.get_user_by_username(
            username=user_creds_login.username
        )
        if user is None:
            raise invalid_credentials_exception

        if not check_hash_password(
            hashed_password=user.hashed_password, password=user_creds_login.password
        ):
            raise invalid_credentials_exception

        access_token = create_access_jwt(user=user)
        refresh_token = create_refresh_jwt(user=user)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def verification_user(self, verif_token: str) -> User:
        check_verif_token: UserToken | None = (
            await self.verif_token_repo.get_verif_token_user(verif_token=verif_token)
        )
        if check_verif_token:
            if (
                datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                > check_verif_token.expires_at
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Verification token has expired",
                )
            user_data: User | False | None = (
                await self.user_repo.change_flag_is_verified(
                    user_id=check_verif_token.user_id,
                )
            )
            if user_data:
                delete_verif_token: bool = (
                    await self.verif_token_repo.delete_user_verif_token(
                        token_id=check_verif_token.id,
                    )
                )
                if delete_verif_token:
                    await self.session.commit()
                    return user_data
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification token invalid"
        )
