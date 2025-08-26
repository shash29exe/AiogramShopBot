from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot_utils.counting_items import counting_items
from database.models import FinallyCarts
from database.utils import db_get_phone, db_session
from config import MANAGER_ID

router = Router()

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """
        Подтверждение заказа
    """

    user = callback.from_user
    user_id = callback.from_user.id
    username = callback.from_user.username
    phone = db_get_phone(user.id)
    mention = f'<a href="https://t.me/{phone}">{user.full_name}</a>'
    user_text = f'{mention}\n{phone} - Заказ подтвержден!'
    context = counting_items(user.id, user_text)

    if not context:
        await callback.message.edit_text('Заказ отсутсвует.')
        await callback.answer()
        return

    if not MANAGER_ID:
        await callback.message.edit_text('Вы не являетесь менеджером.')
        await callback.answer()
        return

    count, text, final_price, cart_id = context

    final_items = db_session.query(FinallyCarts).filter_by(cart_id=cart_id).all()
    orders_summary = '\n'.join([
        f'{item.product_name} - {item.quantity} - {item.final_price}₽'
        for item in final_items
    ])
    await bot.send_message(MANAGER_ID, text, parse_mode='HTML')
    await callback.message.edit_text('Ваш заказ принят, ожидайте обратной связи!')
    await callback.answer('Заказ оформлен!')