from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_utils.text import gen_cart_text
from database.utils import db_get_product_delete, db_increase_product_quantity, db_get_cart_items, \
    db_decrease_product_quantity
from keyboards.inline_kb import cart_action_kb
from keyboards.reply_kb import main_menu_kb

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


@router.callback_query(F.data.startswith('decrease_'))
async def decrease_quantity(callback: CallbackQuery, bot: Bot):
    """
        Уменьшение количества товаров в заказе
    """

    cart_id = int(callback.data.split('_')[1])
    db_decrease_product_quantity(cart_id)

    user_id = callback.from_user.id
    cart_items = db_get_cart_items(user_id)

    if not cart_items:
        try:
            await callback.message.delete()
        except Exception as e:
            print(f'error: {e}')

        try:
            await bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id - 1
            )
        except Exception as e:
            print(f'error: {e}')

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text='Корзина пуста, выберите товар',
            reply_markup=main_menu_kb()
        )

    else:
        text = gen_cart_text(cart_items)
        keyboard = cart_action_kb()

        await callback.message.edit_text(text, reply_markup=keyboard)

    await callback.answer('Количество товара уменьшено')

@router.callback_query(F.data == 'back_to_cart')
async def back_to_cart_cb(callback: CallbackQuery):
    """
        Функция для кнопки назад из меню добавления/удаления товаров
    """

    await callback.message.edit_text('Корзина', reply_markup=cart_action_kb())
    await callback.answer()