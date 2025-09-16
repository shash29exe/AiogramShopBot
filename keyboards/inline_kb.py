from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MANAGER_USERNAME
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
        callback_data='Предварительный заказ'
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
    """
        Кнопка для изменения количества товара в корзине
    """

    builder = InlineKeyboardBuilder()
    builder.button(text='➖', callback_data='action -')
    builder.button(text=str(quantity), callback_data='quantity')
    builder.button(text='➕', callback_data='action +')
    builder.button(text='🛒 В корзину', callback_data='put_in_cart')
    builder.button(text='🔙 Назад', callback_data='back_one_step')

    builder.adjust(3, 1, 1)
    return builder.as_markup()


def cart_action_kb():
    """
        Кнопка для действия с корзиной
    """

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📦 Подтвердить заказ', callback_data='confirm_order'),
        InlineKeyboardButton(text='❌ Удалить товар', callback_data='delete_product'),
        InlineKeyboardButton(text='✔️ Добавить товар', callback_data='add_product'),
        InlineKeyboardButton(text='🔙 Назад', callback_data='back_one_step')
    )

    builder.adjust(1, 2)

    return builder.as_markup()


def settings_kb():
    """
        Подменю настроек
    """

    builder = InlineKeyboardBuilder()
    builder.button(text='🌍 Язык', callback_data='change_language')
    builder.button(text='🧑‍💻 Связь с менеджером', url=f't.me/{MANAGER_USERNAME}')
    builder.button(text='❌ Удалить аккаунт', callback_data='delete_account')

    builder.adjust(1, 1, 1)

    return builder.as_markup()

def confirm_delete_kb():
    """
        Кнопка подтверждения удаления товара:
    """

    builder = InlineKeyboardBuilder()
    builder.button(text='❌ Нет', callback_data='back_to_settings')
    builder.button(text='✅ Да', callback_data='confirm_delete')

    builder.adjust(1, 1)

    return builder.as_markup()