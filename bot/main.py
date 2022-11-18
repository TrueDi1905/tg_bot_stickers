from aiogram.utils import executor

import handlers
from config import dp

handlers.handler_register_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
