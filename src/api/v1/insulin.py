from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Annotated

from core import settings
from core.schemas import ProductList, InsulinDose, ProductCreate, ProductInfo
from core.services import ProductsService


router = APIRouter(prefix=settings.api.v1.insulin, tags=["insulin"])


@router.get("/products/insulin-dose/{products}/", response_model=InsulinDose)
async def get_product_by_name(
    request: Request,
    products: ProductList,
    product_service: Annotated[ProductsService, Depends(ProductsService)],
) -> InsulinDose | HTTPException:
    insulin_dose: dict[str, str] = product_service.calculate_insulin_dose()
    return InsulinDose(**insulin_dose)


@router.post("/products/add/", response_model=ProductInfo)
async def create_product(
    request: Request,
    product_creds: ProductCreate,
    product_service: Annotated[ProductsService, Depends(ProductsService)],
) -> ProductInfo:
    return await product_service.create_user_product(product_creds=product_creds)
