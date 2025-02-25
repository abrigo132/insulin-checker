from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.core.config import settings
from src.core.schemas.users import UserCreate, UserRead, UserLogin
from src.core.models.db_helper import db_helper
from src.core.auth.register.utils import (
    check_confirm_password_with_password,
    check_hash_password,
)
from src.crud.users import UsersCrud
from src.core.models.users import User
from src.core.auth.login.utils import create_access_jwt, create_refresh_jwt
from src.core.schemas.jwt import TokenInfo

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
    user_register = await crud.create_user(session=session, user_create=credentials)
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
