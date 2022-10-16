import io

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_tg import dp
from keyboard import start_menu_keyboard, back_to_menu_keyboard, photo_choice_keyboard, pack_keyboard
from remove_bg import photo_remove_bg


class FSMAdmin(StatesGroup):
    photo = State()
    photo_background = State()
    pack = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Желаешь создать новый стикер?',
                         reply_markup=start_menu_keyboard)


@dp.message_handler(content_types=['text'], text='Создать новый стикер', state=None)
async def create_stickers(message: types.Message):
    await FSMAdmin.photo.set()
    await message.answer('Зарузите фото', reply_markup=back_to_menu_keyboard)


@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    image = io.BytesIO()
    async with state.proxy() as data:
        await message.photo[-1].download(image)
        data['photo'] = message.photo[-1].file_id
    await FSMAdmin.next()
    await message.answer('Хотите удалить задний фон на изображении?',
                         reply_markup=photo_choice_keyboard)


@dp.message_handler(state=FSMAdmin.photo_background)
async def load_name(message: types.Message, state: FSMContext):
    if message.text == 'Удалить фон':
        #await photo_remove_bg(data['photo'])
        print('удаляем фон')
    async with state.proxy() as data:
        data['photo_background'] = True
    await FSMAdmin.next()
    await message.reply('Выберите куда загрузить стикер', reply_markup=pack_keyboard)


@dp.message_handler(state=FSMAdmin.pack)
async def load_photo(message: types.Message, state: FSMContext):
    if message.text == 'Создать новый пак':
        print('Создаем пак')
        print('введите название пака')
    print('Выбрать действующий пак')
    print('пак создан')
    async with state.proxy() as data:
        await message.reply(str(data))
        await state.finish()


@dp.message_handler(state='*', commands='Вернуться в меню')
@dp.message_handler(Text(equals='Вернуться в меню', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await send_welcome(message)


def handler_register_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
