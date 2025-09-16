from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from keyboards.inline_kb import settings_kb

router = Router()

@router.message(F.text == "⚙ Настройки")
async def settings(message: Message):
    """
        Обработчик меню настроек
    """

    await message.answer(text="⚙ Настройки", reply_markup=settings_kb())