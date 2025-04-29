from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from core.config import settings


class DbHelper:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        DbHelper.__instance = None

    def __init__(
        self,
        url: str,
        echo: bool,
        echo_pool: bool,
        max_overflow: int,
        pool_size: int,
    ) -> None:
        if not hasattr(self, "_initialized"):
            self.async_engine: AsyncEngine = create_async_engine(
                url=url,
                echo=echo,
                echo_pool=echo_pool,
                max_overflow=max_overflow,
                pool_size=pool_size,
            )
            self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
                bind=self.async_engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
            self._initialized: bool = True

    async def dispose(self) -> None:
        await self.async_engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper: DbHelper = DbHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)
