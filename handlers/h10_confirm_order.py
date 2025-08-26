from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_phone

router = Router()

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """
        Подтверждение заказа
    """

    user = callback.from_user
    user_id = callback.from_user.id
    username = callback.from_user.username
    phone = db_get_phone(user_id)