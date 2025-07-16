from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from .categories import Categories


class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    image: Mapped[str] = mapped_column(String(200))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2))

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    product_category: Mapped[Categories] = relationship(back_populates='products')

    def __str__(self):
        return self.product_name
