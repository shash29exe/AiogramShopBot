from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from database.utils import db_register_user
from keyboards.reply_kb import start_kb

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


@router.message(Text='Привет')
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

    if db_register_user(chat_id, full_name):
        await message.answer(text=f'Привет👋')

    else:
        await message.answer(text='Для связи с ботом необходимо зарегистрироваться')
