from sqlalchemy import text, select
from sqlalchemy.orm import Session

from database.models import Categories, Products
from database.base import Base, engine
from database.models import Orders

def initial_db():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print('Создание базы данных...')
    Base.metadata.create_all(engine)

    categories = ('Ноутбуки', 'Системные блоки', 'Мониторы')

    products = [
        ('Ноутбуки', 'Ноутбук ASUS ZenBook', 100000, 'Ноутбук ASUS ZenBook UX431FL', 'media/laptops/asus_zenbook.jpg'),
        ('Ноутбуки', 'Ноутбук Lenovo Ideapad', 120000, 'Ноутбук Lenovo Ideapad 330', 'media/laptops/lenovo_ideapad.jpg'),
        ('Системные блоки', 'Системный блок ASUS ROG', 150000, 'Системный блок ASUS ROG Strix G15', 'media/pcs/asus_rog.jpg'),
        ('Системные блоки', 'Системный блок Lenovo Ideapad', 170000, 'Системный блок Lenovo Ideapad Gaming 3',
         'media/pcs/lenovo_ideapad_gaming.jpg'),
        ('Мониторы', 'Монитор ASUS', 10000, 'Монитор ASUS ROG Swift PG27AQN', 'media/monitors/asus_vg278q.jpg'),
        ('Мониторы', 'Монитор Lenovo', 12000, 'Монитор Lenovo VG278Q', 'media/monitors/asus_rog_swift.jpg'),
    ]

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
            category_id = category_map.get(category_name)
            if not category_id:
                continue

            existing_product = session.scalar(
                select(Products).where(
                    Products.product_name == name,
                    Products.category_id == category_id
                )
            )
            if existing_product:
                continue

            product = Products(
                category_id=category_id,
                product_name=name,
                price=price,
                description=description,
                image=image
            )
            session.add(product)

        session.commit()

    print('База данных создана!')


if __name__ == '__main__':
    initial_db()