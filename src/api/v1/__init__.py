from fastapi import APIRouter

from core import settings
from .users import router as user_router
from .insulin import router as insulin_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(user_router)
router.include_router(insulin_router)
