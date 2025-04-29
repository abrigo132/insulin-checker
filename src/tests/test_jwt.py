import pytest

from core.models import User
from core.auth.login import (
    create_access_jwt,
    decode_jwt,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_refresh_jwt,
)


@pytest.fixture
def test_user():
    return User(
        id=1,
        username="test_user",
    )


def test_create_access_jwt_correctly_payload(test_user):
    access_token = create_access_jwt(user=test_user)
    payload = decode_jwt(token=access_token)

    assert payload["id"] == test_user.id
    assert payload["sub"] == test_user.username
    assert payload[TOKEN_TYPE_FIELD] == ACCESS_TOKEN_TYPE


def test_create_refresh_jwt_correctly_payload(test_user):
    refresh_token = create_refresh_jwt(user=test_user)
    payload = decode_jwt(token=refresh_token)

    assert payload["sub"] == test_user.username
    assert payload[TOKEN_TYPE_FIELD] == REFRESH_TOKEN_TYPE
