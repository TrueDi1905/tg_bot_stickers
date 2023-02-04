import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import dotenv_values


TOKEN_BOT = dotenv_values('../.env')['TOKEN_BOT']

storage = MemoryStorage()

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)
