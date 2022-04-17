import asyncio


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import register_handlers_core

TOKEN = "5234240651:AAEXPg_niaSlYc0lZq_nBfZYONLWvYwNdZk"


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_core(dp)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
