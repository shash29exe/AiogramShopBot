from sqlalchemy.orm import Session
from database.base import engine
from database.models import Users
from sqlalchemy.exc import IntegrityError


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
