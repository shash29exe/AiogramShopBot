from aiogram import Router, F, Bot
from aiogram.types import Message

from database.utils import db_get_last_orders
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

    for delete_count in range(3):
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - delete_count
        )

    await get_main_menu(message)


@router.message(F.text == '📖 История заказов')
async def h_history_orders(message: Message):
    """
        реакция на кнопку '📖 История заказов'
    """

    chat_id = message.chat.id

    orders = db_get_last_orders(chat_id)
    if not orders:
        await message.answer(text="У вас нет заказов")
        return

    text = "Ваши заказы:\n\n"
    total_sum = 0
    for order in orders:
        text += f'{order.product_name} - {order.quantity}шт. - {order.final_price:.2f}₽\n'
        total_sum += float(order.final_price)

    text += f'\nОбщая сумма заказов: {total_sum:.2f}₽'

    await message.answer(text=text)