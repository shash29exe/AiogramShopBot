from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from handlers.h03_order import make_order

router = Router()

@router.message(F.text == "↩️ Назад")
async def back(message: Message, bot: Bot):
    """
        Реакция на кнопку "Назад"
    """

    try:
        message_id = message.message_id-1
        await bot.delete_message(chat_id=message.chat.id, message_id=message_id-1)

    except TelegramBadRequest:
        pass

    await make_order(message, bot)
