from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from fastapi import APIRouter, Depends, HTTPException, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from core import settings
from core.schemas import UserCreate, UserRead, UserLogin
from core.models import db_helper
from core.auth.register import (
    check_confirm_password_with_password,
    check_hash_password,
    create_confirm_register_token_url,
)
from crud import UsersCrud
from core.models import User, UserToken
from core.auth.login import create_access_jwt, create_refresh_jwt
from core.schemas import TokenInfo
from tasks import send_verification_message
from crud import VerifToken

router = APIRouter(prefix=settings.api.v1.users)


@router.post("/register/", response_model=UserRead)
async def register_user(
    credentials: UserCreate,
    crud: Annotated[UsersCrud, Depends(UsersCrud)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    if not await check_confirm_password_with_password(
        password=credentials.password,
        confirm_password=credentials.confirm_password,
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Пароли не совпадают"
        )
    user_register: User = await crud.create_user(
        session=session, user_create=credentials
    )
    confirm_token = create_confirm_register_token_url()
    token_register: UserToken = await crud.add_user_token(
        user_id=user_register.id,
        token=confirm_token,
        session=session,
    )
    await send_verification_message.kiq(user_register.id, confirm_token)
    return user_register


@router.post("/login/", response_model=TokenInfo)
async def user_login(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    crud: Annotated[UsersCrud, Depends(UsersCrud)],
    user_credentials: UserLogin = Form(),
) -> TokenInfo:
    invalid_credentials_exception: HTTPException = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    user: User = await crud.get_user_by_username(
        session=session, username=user_credentials.username
    )
    if user is None:
        raise invalid_credentials_exception

    if not check_hash_password(
        hashed_password=user.hashed_password, password=user_credentials.password
    ):
        raise invalid_credentials_exception

    access_token = create_access_jwt(user=user)
    refresh_token = create_refresh_jwt(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/verification/", response_model=UserRead)
async def verified_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    verif_token: str,
    crud_token: Annotated[VerifToken, Depends(VerifToken)],
    crud_user: Annotated[UsersCrud, Depends(UsersCrud)],
):
    check_verif_token: UserToken | None = await crud_token.get_verif_token_user(
        session=session, verif_token=verif_token
    )
    if check_verif_token:
        if (
            datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            > check_verif_token.expires_at
        ):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Verification token has expired",
            )
        user_data: User | False | None = await crud_user.change_flag_is_verifed(
            user_id=check_verif_token.user_id,
            session=session,
        )
        if user_data:
            delete_verif_token: bool = await crud_token.delete_user_verif_token(
                session=session,
                token_id=check_verif_token.id,
            )
            if delete_verif_token:
                return user_data
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail="Verification token invalid"
    )
