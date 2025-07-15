from sqlalchemy import text, select
from sqlalchemy.orm import Session

from database.models import Carts, Users, FinallyCarts, Categories, Products
from database.base import Base, engine


def initial_db():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print('Создание базы данных...')
    Base.metadata.create_all(engine)

    categories = ('Ноутбуки', 'Системные блоки', 'Мониторы')
    products = (
        ('Ноутбуки', 'ASUS', 100000, 'Ноутбук ASUS ZenBook UX431FL', ''),
        ('Ноутбуки', 'Lenovo', 120000, 'Ноутбук Lenovo Ideapad 330', ''),
        ('Системные блоки', 'ASUS', 150000, 'Системный блок ASUS ROG Strix G15', ''),
        ('Системные блоки', 'Lenovo', 170000, 'Системный блок Lenovo Ideapad Gaming 3', ''),
        ('Мониторы', 'ASUS', 10000, 'Монитор ASUS VG278Q', ''),
        ('Мониторы', 'Lenovo', 12000, 'Монитор Lenovo Ideapad Gaming 3', ''),
    )

    with Session(engine) as session:
        category_map = {}

        for name in categories:
            category = session.scalar(select(Categories).where(Categories.category_name == name))
            if not category:
                category = Categories(category_name=name)
                session.add(category)
                session.flush()

            category_map[name] = category.id

        for category_name, name, price, description, image in products:
            existing_product = session.scalar(select(Products).where(Products.product_name == name))

            if existing_product:
                continue

            category_id = category_map.get(category_name)
            if category_id:
                product = Products(
                    category_id=category_id,
                    product_name=name,
                    price=price,
                    description=description,
                    image=image
                )

                session.add(product)

            session.commit()


if __name__ == '__main__':
    initial_db()
    print('База данных создана!')
