from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_user_cart, db_upsert_cart
from handlers.h06_back_button import back

router = Router()

@router.callback_query(F.data == 'put_in_cart')
async def put_in_cart(callback: CallbackQuery, bot: Bot):
    """
        Обработчик добавления товаров в корзину
    """

    chat_id = callback.from_user.id
    message = callback.message

    caption = message.caption
    if not caption:
        await bot.send_message(chat_id=chat_id, text='Товар не найден')
        return

    product_name = caption.split('\n')[0]
    cart = db_get_user_cart(chat_id)
    if not cart:
        await bot.send_message(chat_id=chat_id, text='Добавьте товар в корзину')
        return

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    result = db_upsert_cart(
        cart_id=cart.id,
        product_name=product_name,
        total_products=cart.total_products,
        total_price=cart.total_price
    )

    if result == "inserted":
        await bot.send_message(chat_id=chat_id, text='Товар добавлен в корзину')
    elif result == "updated":
        await bot.send_message(chat_id=chat_id, text='Товар обновлен')
    elif result == "error":
        await bot.send_message(chat_id=chat_id, text='Ошибка добавления товара')

    await back(message, bot)
