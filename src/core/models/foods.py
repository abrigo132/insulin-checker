from .base import Base

from sqlalchemy.orm import Mapped, mapped_column


class Food(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=True)
    calories: Mapped[float] = mapped_column(nullable=True)
    protein: Mapped[float] = mapped_column(nullable=True)
    fat: Mapped[float] = mapped_column(nullable=True)
    carbohydrates: Mapped[float] = mapped_column(nullable=True)
    fiber: Mapped[float] = mapped_column(nullable=True)
    glycemic_index: Mapped[float] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
