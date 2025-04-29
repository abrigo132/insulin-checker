from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    brand: str
    calories: float
    protein: float
    fat: float
    carbohydrates: float
    fiber: float
    glycemic_index: float
    category: str


class ProductInfo(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass
