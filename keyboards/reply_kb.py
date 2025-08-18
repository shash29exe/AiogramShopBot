from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def start_kb():
    """
        Кнопка старта
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет")]
        ],
        resize_keyboard=True
    )

def phone_kb():
    """
        Предоставление номера телефона
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Предоставить номер телефона", request_contact=True)
    return builder.as_markup(resize_keyboard=True)

def main_menu_kb():
    """
        Главное меню
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Оформить заказ")
    builder.button(text="📖 История заказов")
    builder.button(text="🛒 Корзина")
    builder.button(text="⚙ Настройки")
    builder.adjust(1, 3)
    return builder.as_markup(resize_keyboard=True)

def back_to_main_menu():
    """
        Назад в главное меню
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="🏠 Главное меню")
    return builder.as_markup(resize_keyboard=True)

def back_arrow_kb():
    """
        Кнопка назад
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="↩️ Назад")
    return builder.as_markup(resize_keyboard=True)
