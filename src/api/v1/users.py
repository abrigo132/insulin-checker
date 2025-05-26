from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form

from core import settings
from core.schemas import UserRegisterCreds, UserRead, UserLogin
from core.services import UserService
from core.models import User
from core.schemas import TokenInfo


router = APIRouter(prefix=settings.api.v1.users, tags=["users"])


@router.post("/register/", response_model=UserRead)
async def register_user(
    user_credentials: UserRegisterCreds,
    user_service: Annotated[UserService, Depends(UserService)],
) -> User:
    user: User = await user_service.create_user(user_creds=user_credentials)
    return user


@router.post("/login/", response_model=TokenInfo)
async def user_login(
    user_service: Annotated[UserService, Depends(UserService)],
    user_credentials: UserLogin = Form(),
) -> TokenInfo | HTTPException:
    return await user_service.login_user(user_creds_login=user_credentials)


@router.get("/verification/{token}/", response_model=UserRead)
async def verified_user(
    verif_token: str,
    user_service: Annotated[UserService, Depends(UserService)],
) -> User | HTTPException:
    return await user_service.verification_user(verif_token=verif_token)
