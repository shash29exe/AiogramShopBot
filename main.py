import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import h01_start, h02_contact_user

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h01_start.router)
dp.include_router(h02_contact_user.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())