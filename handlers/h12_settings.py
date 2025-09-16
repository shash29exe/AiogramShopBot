from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from keyboards.inline_kb import settings_kb, confirm_delete_kb

router = Router()

@router.message(F.text == "⚙ Настройки")
async def settings(message: Message):
    """
        Обработчик меню настроек
    """

    await message.answer(text="⚙ Настройки", reply_markup=settings_kb())

async def change_language():
    pass

@router.callback_query(F.data == 'delete_account')
async def delete_account(callback: CallbackQuery):
    """
        Удаление аккаунта
    """

    await callback.message.edit_text("Подтвердите удаление аккаунта", reply_markup=confirm_delete_kb())