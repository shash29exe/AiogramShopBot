from sqlalchemy.orm import Session
from database.base import engine
from database.models import Users, Categories, FinallyCarts, Orders, Products
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select, func, join
from database.models import Carts


def get_session():
    return Session(engine)


def db_register_user(fullname, chat_id):
    """
        Функция регистрации пользователя
    """

    try:
        with get_session() as session:
            query = Users(name=fullname, telegram=chat_id)
            session.add(query)
            session.commit()

        return False
    except IntegrityError:
        return True


def db_update_user_phone(chat_id, phone: str):
    """
        Получение номера телефона
    """

    with get_session() as session:
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id):
    """
        Создание корзины пользователя
    """

    try:
        with get_session() as session:
            subquery = session.scalar(select(Users).where(Users.telegram == chat_id))
            query = Carts(user_id=subquery.id)
            session.add(query)
            session.commit()
            return True
    except IntegrityError:
        return False
    except AttributeError:
        return False


def db_get_all_categories():
    """
        Получение всех категорий
    """

    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """
        Получение финальной цены
    """

    with get_session() as session:
        cart = (session.query(Carts)
                .join(Users, Carts.user_id == Users.id).filter(Users.telegram == chat_id).first())
        if not cart:
            return 0

        product_total = (
            session.query(func.coalesce(func.sum(FinallyCarts.final_price), 0))
            .filter(FinallyCarts.cart_id == cart.id)
            .scalar()
        )

        if product_total == 0:
            return 0

        return float(product_total)


def db_get_last_orders(chat_id, limit=10):
    """
         Функция получения последних заказов
    """

    with get_session() as session:
        orders = (
            session.query(Orders)
            .join(Carts, Orders.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .filter(Users.telegram == chat_id)
            .order_by(Orders.id.desc())
            .limit(limit)
            .all()
        )

        return orders


def db_get_product(category_id):
    """
        Получение продуктов по категории
    """

    with get_session() as session:
        query = select(Products).where(Products.category_id == category_id)
        return session.scalars(query).all()


def db_get_product_by_id(product_id):
    """
        Получение продукта по id
    """

    with get_session() as session:
        query = select(Products).where(Products.id == product_id)
        return session.scalar(query)


def db_get_user_cart(chat_id):
    """
        Получение корзины пользователя по id
    """

    with get_session() as session:
        query = select(Carts).join(Users, Carts.user_id == Users.id).where(Users.telegram == chat_id)
        return session.scalar(query)


def db_update_user_cart(price, cart_id, quantity=1):
    """
        Обновление корзины пользователя
    """

    with get_session() as session:
        query = update(Carts).where(Carts.id == cart_id).values(total_price=price, total_products=quantity)
        session.execute(query)
        session.commit()

def db_get_cart_items(chat_id):
    """
        Получение всех товаров из корзины пользователя
    """

    with get_session() as session:
        query = select(FinallyCarts.id,
                       FinallyCarts.product_name,
                       FinallyCarts.final_price,
                       FinallyCarts.quantity,
                       FinallyCarts.cart_id) \
        .join(Carts, FinallyCarts.cart_id == Carts.id) \
        .join(Users, Carts.user_id == Users.id) \
        .where(Users.telegram == chat_id) \
        .group_by(FinallyCarts.id)

        return session.execute(query).mappings().all()