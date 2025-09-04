from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_product_delete, db_increase_product_quantity

router = Router()


@router.callback_query(F.data == "delete_product")
async def delete_product(callback: CallbackQuery):
    """
        Удаление товара из заказа
    """

    chat_id = callback.from_user.id
    cart_products = db_get_product_delete(chat_id)

    builder = InlineKeyboardBuilder()

    for cart_id, name in cart_products:
        builder.button(text=f'➖ {name}', callback_data=f'decrease_{cart_id}')

    builder.button(text='🔙 Назад', callback_data='back_to_cart')
    builder.adjust(1, 1)
    await callback.message.edit_text('Выберете товар для изменения количества',
                                     reply_markup=builder.as_markup())

    await callback.answer()


@router.callback_query(F.data == "add_product")
async def add_product(callback: CallbackQuery):
    """
        Добавление товара в заказ
    """

    chat_id = callback.from_user.id
    cart_products = db_get_product_delete(chat_id)

    builder = InlineKeyboardBuilder()

    for cart_id, name in cart_products:
        builder.button(text=f'➕ {name}', callback_data=f'increase_{cart_id}')

    builder.button(text='🔙 Назад', callback_data='back_to_cart')
    builder.adjust(1)
    await callback.message.edit_text('Выберете товар для изменения количества',
                                     reply_markup=builder.as_markup())

    await callback.answer()


@router.callback_query(F.data.startswith('increase_'))
async def increase_quantity(callback: CallbackQuery):
    """
        Увеличение количества товаров в заказе
    """

    cart_id = int(callback.data.split('_')[1])
    db_increase_product_quantity(cart_id)
    await callback.answer('Количество товара увеличено')
    await add_product(callback)
