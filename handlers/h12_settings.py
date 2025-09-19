from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from config import MANAGER_ID
from database.utils import db_delete_user_by_telegram_id
from keyboards.inline_kb import settings_kb, confirm_delete_kb, change_language_kb
from keyboards.reply_kb import start_kb

router = Router()


@router.message(F.text == "⚙ Настройки")
async def settings(message: Message):
    """
        Обработчик меню настроек
    """

    await message.answer(text="⚙ Настройки", reply_markup=settings_kb())


@router.callback_query(F.data == 'change_language')
async def change_language(callback: CallbackQuery):
    await callback.message.edit_text('Выбор языка', reply_markup=change_language_kb())


@router.callback_query(F.data == 'delete_account')
async def delete_account(callback: CallbackQuery):
    """
        Подменю удаления аккаунта
    """

    await callback.message.edit_text("Подтвердите удаление аккаунта", reply_markup=confirm_delete_kb())


@router.callback_query(F.data == 'confirm_delete')
async def confirm_delete(callback: CallbackQuery, bot: Bot):
    """
        Удаление аккаунта
    """

    telegram_id = callback.from_user.id
    full_name = callback.from_user.full_name

    result, phone = db_delete_user_by_telegram_id(telegram_id)

    if result:
        await bot.send_message(
            chat_id=MANAGER_ID,
            text=f"Пользователь <b>{full_name}</b> ({telegram_id})\n"
                 f"с номером телефона <b>{phone}</b> удалён.",
            parse_mode='HTML'
        )
        await callback.message.answer('Ваш аккаунт успешно удалён.', reply_markup=start_kb())


@router.callback_query(F.data == 'back_to_settings')
async def back_to_settings(callback: CallbackQuery):
    """
        Отмена удаления аккаунта
    """

    await callback.message.delete()
    await callback.message.answer('⚙ Настройки', reply_markup=settings_kb())
