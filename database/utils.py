from sqlalchemy.orm import Session
from database.base import engine
from database.models import Users
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select
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


def db_update_user_phone(chat_id, phone:str):
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