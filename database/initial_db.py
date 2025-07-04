from sqlalchemy import text

from database.models import Carts, Users
from database.base import Base, engine

def initial_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print('Создание базы данных...')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    initial_db()
    print('База данных создана!')
