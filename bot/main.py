import asyncio

from aiogram.utils import executor

from config import dp
from workers import user_chat_worker


async def on_startup(dp):
    asyncio.create_task(user_chat_worker())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
