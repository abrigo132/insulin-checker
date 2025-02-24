from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.core.config import settings
from src.core.schemas.users import UserCreate, UserRead
from src.core.models.db_helper import db_helper
from src.core.auth.register.utils import check_confirm_password_with_password
from src.crud.users import UsersCrud
from src.core.models.users import User

router = APIRouter(prefix=settings.api.v1.users, tags=["users"])


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
