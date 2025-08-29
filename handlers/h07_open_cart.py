from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from database.utils import db_get_cart_items
from keyboards.inline_kb import cart_action_kb

router = Router()

@router.message(F.text == "🛒 Корзина")
async def cart(message: Message):
    """
        Логика корзины
    """

    chat_id = message.chat.id

    await show_cart(chat_id, send_fn=message.answer)

@router.callback_query(F.data == "Предварительный заказ")
async def preorder(callback: CallbackQuery):
    await show_cart(chat_id=callback.from_user.id, send_fn=callback.message.answer)
    await callback.answer()

async def show_cart(chat_id, send_fn):
    """
        Показ корзины заказов
    """

    cart_items = db_get_cart_items(chat_id)

    if not cart_items:
        await send_fn("Ваша корзина пуста")
        return

    text = "Корзина:\n"
    total = 0
    for item in cart_items:
        subtotal = float(item.total_price)
        total += subtotal
        text += f"{item.product_name} - {item.quantity} шт. - {subtotal:.2f}₽\n"
    text += f"\nИтого: {total:.2f} ₽"
    await send_fn(text, reply_markup=cart_action_kb())