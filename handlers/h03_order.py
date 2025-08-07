from aiogram import Router, F, Bot
from aiogram.types import Message

from keyboards.inline_kb import get_category_menu
from keyboards.reply_kb import back_to_main_menu

router = Router()

@router.message(F.text == '📝 Оформить заказ')
async def make_order(message: Message, bot):
    """
        реакция на кнопку '📝 Оформить заказ', редоставление категорий товаров
    """

    chat_id = message.chat.id

    await bot.send_message(chat_id=chat_id,
                           text="Оформляем заказ",
                           reply_markup=back_to_main_menu())
    await message.answer(text="Выберете категорию", reply_markup=get_category_menu(chat_id))
