from fastapi import APIRouter, Request, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.models import db_helper


router = APIRouter(prefix=settings.api.v1.insulin, tags=["insulin"])


@router.get("/products/insulin-dose/{{products}}/", response_model=InsulinDose)
async def get_product_by_name(
    request: Request,
    products: ProductList,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    insulin_dose: dict[str, str] = ProductsService(
        session=session
    ).calculate_insulin_dose()
    return InsulinDose(**insulin_dose)
