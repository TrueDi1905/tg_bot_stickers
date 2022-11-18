import io
import asyncio
import random
import re

import emoji
from pyrogram import Client
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import dp
from image_editor import photo_remove_bg, photo_resize
from keyboard import start_menu_keyboard, \
    back_to_menu_keyboard, photo_choice_keyboard, \
    pack_keyboard, pack_choice, none_pack
from smiles import send_smile
from models import engine, Users, Stickers


class FSMAdmin(StatesGroup):
    photo = State()
    photo_background = State()
    pack = State()
    stick_create = State()


session = Session(bind=engine)
app = Client("my_account")
app.start()


async def send_welcome(message: types.Message):
    text = 'Желаешь создать новый стикер?'
    await message.answer(text, reply_markup=start_menu_keyboard)


@dp.message_handler(state='*', commands='Вернуться в меню')
@dp.message_handler(Text(
    equals='Вернуться в меню', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await send_welcome(message)


@dp.message_handler(content_types=['text'],
                    text='Создать новый стикер', state=None)
async def create_stickers(message: types.Message):
    await FSMAdmin.photo.set()
    text = 'Зарузите фото'
    await message.answer(text, reply_markup=back_to_menu_keyboard)


@dp.message_handler(content_types=['text'], text='Мои стикеры', state=None)
async def my_stickers(message: types.Message):
    get_stickers = engine.execute(
        select([Stickers.stickers_tg]).where(Stickers.tg_users ==
                                             message.from_user.id)).fetchall()
    packs = await pack_choice(get_stickers)
    url = 'https://t.me/addstickers/'
    await message.answer('Ваши стикерпаки 👇')
    text = ''
    for i in get_stickers:
        text += url + "".join(i) + '\n'
    await message.answer(text, reply_markup=back_to_menu_keyboard)


@dp.message_handler(content_types=['photo', 'document'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.document:
        text = 'Пожалуйста, поставьте галочку ' \
               '«Сжать изображение» при отправке фото'
        await message.answer(text)
        return
    image_download = io.BytesIO()
    await message.photo[-1].download(image_download)
    new_photo = await photo_resize(image_download)
    async with state.proxy() as data:
        data['photo'] = new_photo
    await FSMAdmin.next()
    text = 'Хотите удалить задний фон на изображении?'
    await message.answer(text,
                         reply_markup=photo_choice_keyboard)


@dp.message_handler(state=FSMAdmin.photo_background)
async def choice_background(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Удалить фон':
            text = 'Нужно немного подождать'
            await message.answer(text)
            background = await photo_remove_bg(data['photo'])
            data['photo_background'] = True
            data['photo'] = background
        else:
            data['photo_background'] = False
    await FSMAdmin.next()
    text = 'Выберите куда загрузить стикер'
    await message.answer(text, reply_markup=pack_keyboard)


@dp.message_handler(state=FSMAdmin.pack)
async def choice_pack(message: types.Message, state: FSMContext):
    if message.text == 'Создать новый пак':
        text = 'Пожалуйста, введите название для нового набора стикеров'
        async with state.proxy() as data:
            data['pack'] = 'new'
        await message.answer(text)
        await FSMAdmin.next()
    else:
        get_stickers = engine.execute(
            select([Stickers.stickers_tg]).where(
                Stickers.tg_users == message.from_user.id)).fetchall()
        if len(get_stickers) == 0:
            await message.answer('У вас пока нет паков',
                                 reply_markup=none_pack)
            return
        packs = await pack_choice(get_stickers)
        async with state.proxy() as data:
            data['pack'] = 'old'
        await message.answer('Выберите пак', reply_markup=packs)
        await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.stick_create)
async def stick_create(message: types.Message, state: FSMContext):
    if len(message.text) < 5 or re.search(r'[а-яА-Я]', message.text):
        text = 'Название должно быть минимум 5 букв ' \
               'и содержать только английские буквы'
        await message.answer(text)
        return
    await message.answer('Нужно немного подождать')
    state_pack = None
    async with state.proxy() as data:
        state_pack = data
    text_create = '/addsticker' if state_pack['pack'] == 'old' else '/newpack'
    await app.send_message("@Stickers", text_create)
    await asyncio.sleep(1)
    await app.send_message("@Stickers", f'{message.text} @Stickers_Now_Bot')
    await asyncio.sleep(1)
    await app.send_document("@Stickers", state_pack['photo'])
    await asyncio.sleep(1)
    await app.send_message("@Stickers", send_smile())
    if text_create == '/addsticker':
        text = 'Стикер скоро будет добавлен в набор: ' \
                       'https://t.me/addstickers/'
        await message.answer(text + message.text,
                             reply_markup=back_to_menu_keyboard)
    else:
        await asyncio.sleep(1)
        await app.send_message("@Stickers", '/publish')
        await asyncio.sleep(1)
        await app.send_message("@Stickers", '/skip')
        random_number = random.randint(1, message.from_user.id)
        pack_name = 'sticker_bot' if ':' in emoji.demojize(message.text) \
            else message.text
        url_pack = f'{pack_name}_{random_number}'
        await app.send_message("@Stickers", url_pack)
        sticker = Stickers(stickers_tg=url_pack,
                           tg_users=message.from_user.id)
        session.add(sticker)
        session.commit()
        text = 'Ваш набор доступен по ссылке: ' \
               'https://t.me/addstickers/'
        await message.answer(text + url_pack,
                             reply_markup=back_to_menu_keyboard)
    get_user = engine.execute(
                    select([Users]).where(Users.user_tg ==
                                          message.from_user.id)).fetchall()
    if len(get_user) == 0:
        user = Users(user_tg=message.from_user.id)
        session.add(user)
        session.commit()
    await state.finish()


def handler_register_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
