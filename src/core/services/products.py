from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.models import Food
from repositories import ProductRepository
from core.schemas import ProductCreate, ProductInfo, ProductList
from core.models import db_helper


class ProductsService:
    def __init__(self, session: AsyncSession = Depends(db_helper.session_getter)):
        self.session: AsyncSession = session
        self.repository: ProductRepository = ProductRepository(session=self.session)
        self.total_carbohydrates: float = 0.0
        self.all_products: Sequence[Food] | None = None

    async def get_products_from_list(self, products: ProductList) -> None:
        products_id = [product.id for product in products.product_list]
        all_products: Sequence[Food] = await self.repository.get_list(
            product_id_list=products_id
        )
        self.all_products = all_products

    def calculate_insulin_dose(self) -> dict[str, str]:
        pass

    async def create_user_product(self, product_creds: ProductCreate) -> ProductInfo:
        new_product: Food = await self.repository.add(product_info=product_creds)
        return ProductInfo(
            name=new_product.name,
            brand=new_product.brand,
            calories=new_product.calories,
            protein=new_product.protein,
            fat=new_product.fat,
            carbohydrates=new_product.carbohydrates,
            fiber=new_product.fiber,
            glycemic_index=new_product.glycemic_index,
            category=new_product.category,
            id=new_product.id,
        )
