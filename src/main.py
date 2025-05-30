from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn import run

from src.core.config import settings
from src.core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # старт приложения
    yield
    # завершение приложения
    await db_helper.dispose()


app_insulin = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)


if __name__ == "__main__":
    run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
