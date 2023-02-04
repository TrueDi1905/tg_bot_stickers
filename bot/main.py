import asyncio

from aiogram.utils import executor

import handlers
from worker import user_chat_worker
from config import dp

handlers.handler_register_client(dp)


async def on_startup(dp):
    asyncio.create_task(user_chat_worker())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
