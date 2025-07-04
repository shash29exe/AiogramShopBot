from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from .users import Users

class Carts(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(7, 2), default=0)
    total_products: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user_cart: Mapped[Users] = relationship(backpopulates='carts')

    def __str__(self):
        return self.id