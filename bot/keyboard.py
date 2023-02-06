from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#Меню
my_stickers = KeyboardButton(text='Мои стикеры')
start_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu_keyboard.add(my_stickers)


#Выход из FSM
cancel_state_button = KeyboardButton(text='Вернуться в меню')
back_to_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_to_menu_keyboard.add(cancel_state_button)


#Развилка на удаление фона
continue_button = KeyboardButton(text='Не удалять фон')
delete_bg_button = KeyboardButton(text='Удалить фон')
photo_choice_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
photo_choice_keyboard.add(continue_button, delete_bg_button)
photo_choice_keyboard.add(cancel_state_button)


#Развилка выбора пака
new_pack_button = KeyboardButton(text='Создать новый пак')
choice_pack = KeyboardButton(text='Выбрать действующий пак')
pack_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
pack_keyboard.add(new_pack_button, choice_pack)
pack_keyboard.add(cancel_state_button)


#Выбор действующих паков
none_pack = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
none_pack.add(new_pack_button, cancel_state_button)


#Мои стикеры
async def pack_choice(get_stickers):
    pack_choice_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
    for pack in get_stickers:
        pack_choice_keyboard.add(KeyboardButton(text="".join(pack)))
    pack_choice_keyboard.add(cancel_state_button)
    return pack_choice_keyboard
