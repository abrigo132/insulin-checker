from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult

from core.models import Food
from core.schemas import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Food

    async def get(self, product_name: str) -> Food | None:
        stmt = select(self.model).where(self.model.name == product_name)
        result: ScalarResult[Food] = await self.session.scalars(statement=stmt)
        return result.one_or_none()

    async def add(self, product_info: ProductCreate):
        self.session.add(product_info)
        await self.session.commit()
