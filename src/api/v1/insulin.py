from fastapi import APIRouter, Request, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.models import db_helper


router = APIRouter(prefix=settings.api.v1.insulin, tags=["insulin"])


@router.get("/products/{{name}}/")
async def get_product_by_name(
    request: Request,
    name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    pass
