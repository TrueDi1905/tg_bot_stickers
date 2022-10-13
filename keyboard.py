from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


create_stickers_button = KeyboardButton(text='Создать новый стикер')
my_stickers = KeyboardButton(text='Мои стикеры')

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(create_stickers_button, my_stickers)
