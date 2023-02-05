import asyncio
import logging

from aiogram.utils import exceptions, executor
from sqlalchemy import select

from bot.models import engine, Users
from bot.config import bot, dp

log = logging.getLogger('broadcast')


def get_users():
    get_user = engine.execute(select([Users.user_tg]))
    users = [row[0] for row in get_user]
    yield from (users)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    count = 0
    try:
        for user_id in get_users():
            if await send_message(user_id, 'Привет! Это рассылка!'):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


if __name__ == '__main__':
    executor.start(dp, broadcaster())
