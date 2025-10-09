from aiogram import Router, F
from aiogram.types import Message
from database.utils import db_update_user_phone, db_create_user_cart
from keyboards.reply_kb import main_menu_kb
from log_action import log_user_phone

router = Router()

@router.message(F.contact)
async def contact_handler(message: Message):
    """
        Получение контакта
    """

    username = message.from_user.username
    chat_id = message.chat.id
    phone = message.contact.phone_number

    db_update_user_phone(chat_id, phone)

    log_user_phone(username=username, user_id=chat_id, phone=phone)

    if db_create_user_cart(chat_id):
        await message.answer(text="Вы успешно зарегистрированы!")

    await get_main_menu(message)

async def get_main_menu(message: Message):
    """
        Демонестрация главного меню
    """

    await message.answer(text="Выберите пункт меню", reply_markup=main_menu_kb())