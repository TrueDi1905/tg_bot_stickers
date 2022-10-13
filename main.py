from aiogram.utils import executor

import handlers, admin
from bot_tg import dp

handlers.handler_register_client(dp)
admin.handler_register_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
