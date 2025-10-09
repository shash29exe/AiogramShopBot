from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from database.utils import db_register_user
from handlers.h02_contact_user import get_main_menu
from keyboards.reply_kb import start_kb, phone_kb
from log_action import log_register_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """
        Реакция на команду start
    """

    photo = FSInputFile('media/welcome.jpg')

    await message.answer_photo(
        photo=photo,
        caption=f'Добро пожаловать, <b>{message.from_user.full_name}</b>!',
        parse_mode='HTML',
        reply_markup=start_kb()
    )


@router.message(F.text == 'Привет')
async def handle_start_button(message: Message):
    """
        Реакция на нажатие кнопки "Привет"
    """

    await handle_start(message)


async def handle_start(message: Message):
    await register(message)


async def register(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name

    log_register_user(username=full_name, user_id=chat_id)

    if db_register_user(full_name, chat_id):
        await message.answer(text=f'Привет👋')
        await get_main_menu(message)

    else:
        await message.answer(text='Для связи с ботом необходимо зарегистрироваться',
                             reply_markup=phone_kb())

