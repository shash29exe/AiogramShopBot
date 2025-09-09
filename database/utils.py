from sqlalchemy.orm import Session
from sqlalchemy import update, select, func, delete
from sqlalchemy.exc import IntegrityError
from database.base import engine
from database.models import Users, Categories, FinallyCarts, Orders, Products
from database.models import Carts


def get_session():
    return Session(engine)


def db_register_user(fullname, chat_id):
    """Функция регистрации пользователя"""
    try:
        with Session(engine) as session:
            user = Users(name=fullname, telegram=chat_id)
            session.add(user)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_get_phone(chat_id):
    """Получение номера телефона"""
    with Session(engine) as session:
        result = session.execute(select(Users.phone).where(Users.telegram == chat_id)).fetchone()
        return result[0] if result else None


def db_update_user_phone(chat_id, phone: str):
    """Изменение номера телефона"""
    with Session(engine) as session:
        session.execute(update(Users).where(Users.telegram == chat_id).values(phone=phone))
        session.commit()


def db_create_user_cart(chat_id):
    """Создание корзины пользователя"""
    try:
        with Session(engine) as session:
            user = session.scalar(select(Users).where(Users.telegram == chat_id))
            if not user:
                return False
            cart = Carts(user_id=user.id)
            session.add(cart)
            session.commit()
            return True
    except (IntegrityError, AttributeError):
        return False


def db_get_all_categories():
    """Получение всех категорий"""
    with Session(engine) as session:
        return session.scalars(select(Categories)).all()


def db_get_finally_price(chat_id):
    """Получение финальной цены корзины"""
    with Session(engine) as session:
        cart = session.query(Carts).join(Users).filter(Users.telegram == chat_id).first()
        if not cart:
            return 0
        total = session.query(func.coalesce(func.sum(FinallyCarts.total_price), 0)) \
            .filter(FinallyCarts.cart_id == cart.id).scalar()
        return float(total) if total else 0


def db_get_last_orders(chat_id, limit=10):
    """Получение последних заказов"""
    with Session(engine) as session:
        return (session.query(Orders)
                .join(Carts, Orders.cart_id == Carts.id)
                .join(Users, Carts.user_id == Users.id)
                .filter(Users.telegram == chat_id)
                .order_by(Orders.id.desc())
                .limit(limit)
                .all())


def db_get_product(category_id):
    """Получение продуктов по категории"""
    with Session(engine) as session:
        return session.scalars(select(Products).where(Products.category_id == category_id)).all()


def db_get_product_by_id(product_id):
    """Получение продукта по id"""
    with Session(engine) as session:
        return session.scalar(select(Products).where(Products.id == product_id))


def db_get_product_by_name(product_name):
    """Получение продукта по имени"""
    with Session(engine) as session:
        return session.scalar(select(Products).where(Products.product_name == product_name))


def db_get_user_cart(chat_id):
    """Получение корзины пользователя по id"""
    with Session(engine) as session:
        return session.scalar(select(Carts).join(Users, Carts.user_id == Users.id).where(Users.telegram == chat_id))


def db_update_user_cart(price, cart_id, quantity=1):
    """Обновление корзины пользователя"""
    with Session(engine) as session:
        session.execute(update(Carts).where(Carts.id == cart_id)
                        .values(total_price=price, total_products=quantity))
        session.commit()


def db_get_cart_items(chat_id):
    """Получение всех товаров из корзины пользователя"""
    with Session(engine) as session:
        return session.execute(
            select(FinallyCarts.id,
                   FinallyCarts.product_name,
                   FinallyCarts.total_price,
                   FinallyCarts.quantity,
                   FinallyCarts.cart_id)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .where(Users.telegram == chat_id)
            .group_by(FinallyCarts.id)
        ).mappings().all()


def db_get_cart_item(cart_id: int, product_name: str):
    """Получение конкретного товара из корзины"""
    with get_session() as session:
        return session.query(FinallyCarts).filter_by(cart_id=cart_id, product_name=product_name).first()


def db_update_cart_item(cart_id: int, product_name: str, quantity: int, product_price: float):
    """Обновление количества и цены конкретного товара в корзине"""
    with get_session() as session:
        item = session.query(FinallyCarts).filter_by(cart_id=cart_id, product_name=product_name).first()
        if not item:
            return False
        item.quantity = quantity
        item.total_price = quantity * float(product_price)
        session.commit()
        return True


def db_update_user_cart_totals(cart_id: int):
    """Пересчет total_price и total_products корзины"""
    with get_session() as session:
        cart = session.query(Carts).filter_by(id=cart_id).first()
        if not cart:
            return False
        totals = session.query(
            func.coalesce(func.sum(FinallyCarts.total_price), 0),
            func.coalesce(func.sum(FinallyCarts.quantity), 0)
        ).filter(FinallyCarts.cart_id == cart_id).first()

        cart.total_price = float(totals[0])
        cart.total_products = int(totals[1])
        session.commit()
        return True


def db_upsert_cart(cart_id, product_name, total_price, total_products):
    """Добавление или обновление товара в корзине"""
    try:
        with Session(engine) as session:
            item = session.query(FinallyCarts).filter_by(cart_id=cart_id, product_name=product_name).first()
            if item:
                item.quantity = total_products
                item.total_price = total_price
                session.commit()
                return 'updated'
            new_item = FinallyCarts(cart_id=cart_id,
                                    product_name=product_name,
                                    quantity=total_products,
                                    total_price=total_price)
            session.add(new_item)
            session.commit()
            return 'inserted'
    except Exception as e:
        print("Ошибка в db_upsert_cart:", e)
        return "error"


def db_get_products_from_final_cart(chat_id):
    """Получение товаров из финальной корзины"""
    with Session(engine) as session:
        return session.execute(
            select(FinallyCarts.product_name,
                   FinallyCarts.quantity,
                   FinallyCarts.total_price,
                   FinallyCarts.cart_id)
            .join(Carts).join(Users)
            .where(Users.telegram == chat_id)
        ).fetchall()


def db_clear_finally_cart(chat_id):
    """Очистка финальной корзины"""
    with get_session() as session:
        cart = session.scalar(select(Carts).join(Users).where(Users.telegram == chat_id))
        if not cart:
            return
        session.execute(delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id))
        session.commit()


def db_save_order_history(chat_id):
    """Сохранение истории заказов"""
    with get_session() as session:
        cart = session.scalar(select(Carts).join(Users).where(Users.telegram == chat_id))
        if not cart:
            return
        final_items = session.query(FinallyCarts).filter_by(cart_id=cart.id).all()
        for item in final_items:
            session.add(
                Orders(
                    cart_id=cart.id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    final_price=item.total_price
                )
            )
        session.commit()


def db_get_product_delete(chat_id):
    """
        Удаление товара из заказа
    """

    with get_session() as session:
        query = select(FinallyCarts.id, FinallyCarts.product_name) \
            .join(Carts).join(Users).where(Users.telegram == chat_id)

        return session.execute(query).fetchall()


def db_increase_product_quantity(finally_cart_id):
    """
        Увеличение количества товаров в заказе
    """

    with get_session() as session:
        item = session.execute(
            select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity += 1
        item.total_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_decrease_product_quantity(finally_cart_id):
    with get_session() as session:
        item = session.execute(
            select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity -= 1

        if item.quantity <= 0:
            session.delete(item)

        else:
            item.total_price = float(product.price) * item.quantity

        session.commit()
        return True