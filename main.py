import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import h01_start, h02_contact_user, h03_order, h04_categories, h05_product_detail

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h01_start.router)
dp.include_router(h02_contact_user.router)
dp.include_router(h03_order.router)
dp.include_router(h04_categories.router)
dp.include_router(h05_product_detail.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())