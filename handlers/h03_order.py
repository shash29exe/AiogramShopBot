from aiogram import Router, F, Bot
from aiogram.types import Message

from handlers.h02_contact_user import get_main_menu
from keyboards.inline_kb import get_category_menu
from keyboards.reply_kb import back_to_main_menu

router = Router()


@router.message(F.text == '📝 Оформить заказ')
async def make_order(message: Message, bot: Bot):
    """
        реакция на кнопку '📝 Оформить заказ', предоставление категорий товаров
    """

    chat_id = message.chat.id

    await bot.send_message(chat_id=chat_id,
                           text="Оформляем заказ",
                           reply_markup=back_to_main_menu())
    await message.answer(text="Выберете категорию", reply_markup=get_category_menu(chat_id))


@router.message(F.text == '🏠 Главное меню')
async def h_main_menu(message: Message, bot: Bot):
    """
        реакция на кнопку '🏠 Главное меню'
    """

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id - 1)

    await get_main_menu(message)


@router.message(F.text == '📖 История заказов')
async def h_history_orders(message: Message):
    """
        реакция на кнопку '📖 История заказов'
    """

    chat_id = message.chat.id


