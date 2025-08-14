from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_all_categories, db_get_finally_price, db_get_product


def get_category_menu(chat_id):
    """
        Инлайн-клавиатура с категориями
    """

    categories = db_get_all_categories()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'Корзина заказа ({total_price if total_price else 0}р.)',
        callback_data='Корзина заказа'
    )
    [builder.button(text=category.category_name, callback_data=f'category_{category.id}')
     for category in categories]

    builder.adjust(1, 2)
    return builder.as_markup()


def show_products(category_id: int):
    """
        Показ продуктов по категориям
    """

    products = db_get_product(category_id)
    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name, callback_data=f'product_{product.id}')
     for product in products]
    builder.adjust(1, 1)
    builder.row(InlineKeyboardButton(text='Назад', callback_data='Назад к категориям'))
    return builder.as_markup()

def quantity_button(quantity=1):
    pass