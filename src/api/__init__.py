from fastapi import APIRouter

from src.core.config import settings
from .v1 import router as v1_router

router = APIRouter(prefix=settings.api.prefix, tags=["api"])

router.include_router(v1_router)
