import pytest
from httpx import post


from core.schemas import UserCreate, UserLogin


@pytest.fixture
def base_url():
    return "http://localhost:8080/api/v1/users/"


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_create_user(base_url: str):
    user_data = UserCreate(
        username="test_user",
        email="test@example.com",
        weight=80,
        password="secret",
        confirm_password="secret",
    )
    url_register = base_url + "register/"
    response = post(url=url_register, json=user_data.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert response_json["username"] == "test_user"
    assert response_json["email"] == "test@example.com"
    assert response_json["weight"] == 80


@pytest.mark.dependency(depends=["test_create_user"])
@pytest.mark.asyncio
async def test_login_user(base_url):
    user_data = UserLogin(username="test_user", password="secret")
    url_login = base_url + "login/"
    response = post(url=url_login, data=user_data.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    assert "refresh_token" in response_json
    assert response_json["token_type"] == "Bearer"
