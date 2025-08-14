from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from bot_utils.text import text_for_caption
from database.utils import db_get_product_by_id, db_get_user_cart, db_update_user_cart
from keyboards.inline_kb import quantity_button
from keyboards.reply_kb import back_to_main_menu

router = Router()

@router.callback_query(F.data.contains('product_'))
async def show_product_detail(callback: CallbackQuery, bot: Bot):
    """
        Подробная информация о товаре
    """

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await bot.delete_message(chat_id, message_id)
    product_id = int(callback.data.split('_')[-1])

    product = db_get_product_by_id(product_id)
    user_cart = db_get_user_cart(chat_id)

    if user_cart:
        db_update_user_cart(price=product.price, cart_id=user_cart.id)
        caption = text_for_caption(product.product_name, product.description, product.price)
        product_image = FSInputFile(path=product.image)

        await bot.send_message(chat_id=chat_id, text='Выберите товар', reply_markup=back_to_main_menu())

        await bot.send_photo(chat_id=chat_id, photo=product_image, caption=caption, parse_mode='HTML', reply_markup=quantity_button())
