import datetime
from datetime import timedelta

import jwt
from typing import TypeVar
from core.config import settings
from core.models.users import User

T = TypeVar("T")

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> T:
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded


def create_jwt(
    token_data: dict,
    token_type: str,
    expire: int = settings.jwt.access_token_expire_minutes,
):
    jwt_payload: dict = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=token_data, expire_minutes=expire)


def create_access_jwt(user: User):
    jwt_payload = {"id": user.id, "sub": user.username, "email": user.email}
    return create_jwt(
        token_data=jwt_payload,
        token_type=ACCESS_TOKEN_TYPE,
        expire=settings.jwt.access_token_expire_minutes,
    )


def create_refresh_jwt(user: User):
    jwt_payload = {"sub": user.username}
    return create_jwt(
        token_data=jwt_payload,
        token_type=REFRESH_TOKEN_TYPE,
        expire=settings.jwt.refresh_token_expire_days,
    )
