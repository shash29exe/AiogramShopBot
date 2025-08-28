from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import MANAGER_ID

from bot_utils.counting_items import counting_items
from database.utils import db_get_phone

router = Router()


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    phone = db_get_phone(user.id)
    mention = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
    user_text = f"Новый заказ от {mention}\nс номером телефона {phone}!"

    context = counting_items(user.id, user_text)
    print(context)

    if not context:
        await callback.message.edit_text('Корзина пуста, оформление заказа невозможно!')
        await callback.answer()
        return

    if not MANAGER_ID:
        await callback.message.edit_text("Менеджер не указан!")
        await callback.answer()
        return

    count, text, total_price, cart_id = context
    await bot.send_message(MANAGER_ID, text, parse_mode="HTML")

    await callback.message.edit_text(
        "Ваш заказ принят! Ожидайте обратной связи от менеджера!\n"
        "Для связи с менеджером, воспользуйтесь кнопкой в настройках"
    )
    await callback.answer("Заказ оформлен! ")
