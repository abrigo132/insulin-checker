from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    InvalidTokenError,
)
from requests import session

from core.auth.login import decode_jwt
from repositories import UserRepository
from core.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/")


async def validate_access_token(
    access_token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(UserRepository),
):
    try:
        access_token_payload = decode_jwt(access_token)
        token_type = access_token_payload.get("type")
        if token_type != "access":
            raise HTTPException(status_code=403, detail="Invalid token type")

        user_id: int = access_token_payload["id"]
        user: User | None = await user_repository.get_user_by_id(user_id=user_id)

        if not user or not user.is_active or not user.is_verified:
            raise HTTPException(status_code=403, detail="User inactive or deleted")
        return user

    except (InvalidSignatureError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
        )
