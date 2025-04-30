from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult, Sequence

from core.models import Food
from core.schemas import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Food

    async def get(self, product_id: str) -> Food | None:
        stmt = select(self.model).where(self.model.name == product_id)
        result: ScalarResult[Food] = await self.session.scalars(statement=stmt)
        return result.one_or_none()

    async def add(self, product_info: ProductCreate) -> Food:
        product: Food = Food(**product_info.model_dump())
        self.session.add(product)
        await self.session.commit()
        return product

    async def get_list(self, product_id_list: list[int]) -> Sequence[Food]:
        stmt = select(self.model).where(self.model.id.in_(product_id_list))
        products: ScalarResult[Food] = await self.session.scalars(statement=stmt)
        return products.all()
