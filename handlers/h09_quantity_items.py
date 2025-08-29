from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from bot_utils.text import text_for_caption
from database.utils import db_get_product_by_name, db_get_user_cart
from database.utils import db_get_cart_item, db_update_cart_item, db_update_user_cart_totals
from keyboards.inline_kb import quantity_button

router = Router()


@router.callback_query(F.data.regexp(r'action [+-]'))
async def change_quantity_products(callback: CallbackQuery, bot: Bot):
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    action = callback.data.split()[-1]

    product_name = callback.message.caption.split('\n')[0]

    product = db_get_product_by_name(product_name)
    user_cart = db_get_user_cart(chat_id)

    if not product or not user_cart:
        await callback.answer("Товар или корзина не найдены!")
        return

    cart_item = db_get_cart_item(user_cart.id, product.product_name)
    if not cart_item:
        await callback.answer("Товар не найден в вашей корзине!")
        return

    current_quantity = cart_item.quantity
    new_quantity = current_quantity

    if action == '+':
        new_quantity += 1
    elif action == '-' and current_quantity > 1:
        new_quantity -= 1
    elif action == '-' and current_quantity <= 1:
        await callback.answer("В корзине минимум 1 товар, удаление невозможно !", show_alert=True)
        return

    db_update_cart_item(user_cart.id, product.product_name, new_quantity, float(product.price))

    db_update_user_cart_totals(user_cart.id)

    caption = text_for_caption(
        name=product.product_name,
        description=product.description,
        price=new_quantity * float(product.price)
    )

    try:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                media=FSInputFile(product.image),
                caption=caption,
                parse_mode='HTML'
            ),
            reply_markup=quantity_button(new_quantity)
        )
    except TelegramBadRequest:
        pass
