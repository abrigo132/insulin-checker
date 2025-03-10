from fastapi import APIRouter

from core import settings
from .users import router as user_router

router = APIRouter(prefix=settings.api.v1.prefix, tags=["api"])

router.include_router(user_router)
