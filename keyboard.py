from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#Меню
create_stickers_button = KeyboardButton(text='Создать новый стикер')
my_stickers = KeyboardButton(text='Мои стикеры')
start_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu_keyboard.add(create_stickers_button, my_stickers)


#Выход из FSM
cancel_state_button = KeyboardButton(text='Вернуться в меню')
back_to_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_to_menu_keyboard.add(cancel_state_button)


#Развилка на удаление фона
continue_button = KeyboardButton(text='Продолжить')
delete_bg_button = KeyboardButton(text='Удалить фон')
photo_choice_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
photo_choice_keyboard.add(continue_button, delete_bg_button)


#Развилка выбора пака
new_pack_button = KeyboardButton(text='Создать новый пак')
choice_pack = KeyboardButton(text='Выбрать действующий пак')
pack_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
pack_keyboard.add(new_pack_button, choice_pack)
