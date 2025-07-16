from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


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
