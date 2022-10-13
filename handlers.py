import io

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_tg import dp
from keyboard import menu
from remove_bg import photo_remove_bg


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Желаешь создать новый стикер?',
                         reply_markup=menu)


@dp.message_handler(content_types=['text'], text='Создать новый стикер', state=None)
async def send_photo(message: types.Message):
    await FSMAdmin.photo.set()
    await message.answer('Зарузите фото', reply_markup=menu)


@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def parser_photo(message: types.Message):
    image = io.BytesIO()
    await message.photo[-1].download(image)
    #await photo_remove_bg(image)
    await message.answer('Хотите удалить задний фон на изображении?')


def handler_register_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
