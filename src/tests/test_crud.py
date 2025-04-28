import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from core import settings
from crud import UsersCrud
from core.schemas import UserCreate



@pytest_asyncio.fixture(scope="module")
async def sqla_async_engine():
    engine: AsyncEngine = create_async_engine(str(settings.db.url))
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def sqla_session_factory(sqla_async_engine) -> async_sessionmaker[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=sqla_async_engine,
        autoflush=False,
        expire_on_commit=False,
    )
    return session_factory


@pytest.fixture(scope="module")
def user_crud():
    users_crud = UsersCrud()
    return users_crud


@pytest.fixture(scope="module")
def test_user():
    return UserCreate(
        username="test_user2",
        email="test2@example.com",
        weight=80,
        password="secret",
        confirm_password="secret",
    )


@pytest_asyncio.fixture(scope="module")
async def create_user(sqla_session_factory, user_crud, test_user):
    async with sqla_session_factory() as session:
        async with session.begin():
            user = await user_crud.create_user(session=session, user_create=test_user)
        await session.close()
        return user.id


@pytest_asyncio.fixture(scope="module", autouse=True)
async def cleanup(sqla_async_engine, create_user):
    yield
    async with sqla_async_engine.begin() as conn:  # Используем begin() вместо connect()
        await conn.execute(
            text("DELETE FROM users WHERE id = :user_id"), {"user_id": create_user}
        )


@pytest.mark.asyncio
async def test_get_user_by_id(sqla_session_factory, user_crud, create_user, test_user):
    async with sqla_session_factory() as session:
        user = await user_crud.get_user_by_id(session=session, user_id=create_user)
        assert user.id == create_user
        assert user.username == test_user.username
        await session.close()


@pytest.mark.asyncio
async def test_get_user_by_username(
    sqla_session_factory, user_crud, test_user, create_user
):

    async with sqla_session_factory() as session:
        user = await user_crud.get_user_by_username(
            session=session, username=test_user.username
        )
        assert user.username == test_user.username
        await session.close()
