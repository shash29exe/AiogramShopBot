from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
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
