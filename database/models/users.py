from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default='ru')

    def __str__(self):
        return self.name