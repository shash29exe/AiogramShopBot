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