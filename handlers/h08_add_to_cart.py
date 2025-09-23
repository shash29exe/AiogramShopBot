from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_user_cart, db_upsert_cart, db_update_user_cart_totals
from handlers.h06_back_button import back

router = Router()


@router.callback_query(F.data == "put_in_cart")
async def add_to_cart(callback: CallbackQuery, bot: Bot):
    chat_id = callback.from_user.id
    message = callback.message
    caption = message.caption

    if not caption:
        await bot.send_message(chat_id=chat_id, text="Товар не найден!")
        return

    product_name = caption.split("\n")[0]
    cart = db_get_user_cart(chat_id)
    if not cart:
        await bot.send_message(chat_id=chat_id, text="Корзина не найдена!")
        return

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    quantity_to_add = 2

    result = db_upsert_cart(
        cart_id=cart.id,
        product_name=product_name,
        quantity=quantity_to_add
    )

    if result in ["inserted", "updated"]:
        db_update_user_cart_totals(cart.id)

    match result:
        case "inserted":
            await bot.send_message(chat_id=chat_id, text="Товар добавлен в корзину!")
        case "updated":
            await bot.send_message(chat_id=chat_id, text="Количество обновлено!")
        case "error":
            await bot.send_message(chat_id=chat_id, text="Ошибка!")

    await back(message, bot)
