from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from keyboards.inline_kb import show_products, get_category_menu

router = Router()


@router.callback_query(F.data.regexp(r'^category_(\d+)$'))
async def show_product_button(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    category_id = int(callback.data.split('_')[-1])

    try:
        await callback.bot.edit_message_text(
            text='Выберите товар',
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=show_products(category_id)
        )
    except TelegramBadRequest:
        await callback.answer("Нет категории")


@router.callback_query(F.data == 'Назад к категориям')
async def back_to_category_button(callback: CallbackQuery):
    """
        Возврат к категориям
    """

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await callback.bot.edit_message_text(
        text='Выберите категорию',
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=get_category_menu(chat_id)
    )