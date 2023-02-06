import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import select

from config import dp
from models import engine, Stickers
from image_editor import photo_remove_bg, photo_resize
from keyboard import start_menu_keyboard, \
    back_to_menu_keyboard, photo_choice_keyboard, \
    pack_keyboard, pack_choice, none_pack


class FSMAdmin(StatesGroup):
    photo = State()
    photo_background = State()
    pack = State()
    stick_create = State()


class StickersCreate:
    def __init__(self, message, pack_option, photo):
        self.message = message
        self.pack_option = pack_option
        self.photo = photo


class Queue:
    stickers = []


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    text = 'Загрузи сюда фото, что бы создать стикер 👇'
    await message.answer(text, reply_markup=start_menu_keyboard)


@dp.message_handler(state='*', commands='Вернуться в меню')
@dp.message_handler(Text(
    equals='Вернуться в меню', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await send_welcome(message)


@dp.message_handler(content_types=['text'], text='Мои стикеры', state=None)
async def my_stickers(message: types.Message):
    get_stickers = engine.execute(
        select([Stickers.stickers_tg]).where(Stickers.tg_users ==
                                             message.from_user.id)).fetchall()
    if len(get_stickers) == 0:
        await message.answer('У вас пока нет стикеров(',
                             reply_markup=back_to_menu_keyboard)
        return
    packs = await pack_choice(get_stickers)
    url = 'https://t.me/addstickers/'
    text = ''
    await message.answer('Ваши стикерпаки 👇')
    for i in get_stickers:
        text += url + "".join(i) + '\n'
    await message.answer(text, reply_markup=back_to_menu_keyboard)


@dp.message_handler(content_types=['photo', 'document'], state=None)
async def load_photo(message: types.Message, state: FSMContext):
    await FSMAdmin.first()
    if message.document:
        text = 'Пожалуйста, поставьте галочку ' \
               '«Сжать изображение» при отправке фото'
        await message.answer(text)
        return
    new_photo = await photo_resize(message.photo[-1])
    async with state.proxy() as data:
        data['photo'] = new_photo
    text = 'Хотите удалить задний фон на изображении?'
    await message.answer(text, reply_markup=photo_choice_keyboard)
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.photo_background)
async def choice_background(message: types.Message, state: FSMContext):
    if message.text == 'Удалить фон':
        await message.answer('Нужно немного подождать')
        async with state.proxy() as data:
            data['photo'] = await photo_remove_bg(data['photo'])
    text = 'Выберите куда загрузить стикер'
    await message.answer(text, reply_markup=pack_keyboard)
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.pack)
async def choice_pack(message: types.Message, state: FSMContext):
    if message.text == 'Создать новый пак':
        async with state.proxy() as data:
            data['pack'] = 'new'
        text = 'Пожалуйста, введите название для нового набора стикеров'
        await message.answer(text)
        await FSMAdmin.next()
    else:
        get_stickers = engine.execute(
            select([Stickers.stickers_tg]).where(
                Stickers.tg_users == message.from_user.id)).fetchall()
        if len(get_stickers) == 0:
            text = 'У вас пока нет паков'
            await message.answer(text, reply_markup=none_pack)
            return
        packs = await pack_choice(get_stickers)
        async with state.proxy() as data:
            data['pack'] = 'old'
        await message.answer('Выберите пак', reply_markup=packs)
        await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.stick_create)
async def stick_create(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        state_pack = data
    if state_pack['pack'] == 'old':
        pack_option = '/addsticker'
        text = 'Стикер скоро будет добавлен в набор: ' \
                       'https://t.me/addstickers/'
        await message.answer(text + message.text,
                             reply_markup=back_to_menu_keyboard)
    else:
        pack_option = '/newpack'
        await message.answer('Нужно немного подождать')
    photo = state_pack['photo']
    sicker = StickersCreate(message, pack_option, photo)
    Queue.stickers.append(sicker)
    await state.finish()
