import asyncio
import random
import emoji

from pyrogram import Client
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Stickers, engine, Users
from handlers import Queue
from keyboard import back_to_menu_keyboard
from smiles import send_smile


session = Session(bind=engine)


async def user_chat_worker():
    app = Client("my_account")
    async with app:
        while True:
            if len(Queue.stickers) > 0:
                item = Queue.stickers.pop()
                message = item.message
                pack_option = item.pack_option
                photo = item.photo
                await app.send_message("@Stickers", pack_option)
                await asyncio.sleep(1)
                await app.send_message("@Stickers", f'{message.text}')
                await asyncio.sleep(1)
                await app.send_document("@Stickers", photo)
                await asyncio.sleep(1)
                await app.send_message("@Stickers", send_smile())
                if pack_option == '/addsticker':
                    url_pack = message.text
                    sticker = Stickers(stickers_tg=url_pack,
                                       tg_users=message.from_user.id)
                    session.add(sticker)
                    session.commit()
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
                    get_user = engine.execute(
                        select([Users]).where(Users.user_tg ==
                                              message.from_user.id)).fetchall()
                    if len(get_user) == 0:
                        user = Users(user_tg=message.from_user.id)
                        session.add(user)
                        session.commit()
                    sticker = Stickers(stickers_tg=url_pack,
                                       tg_users=message.from_user.id)
                    session.add(sticker)
                    session.commit()
                    text = 'Ваш набор доступен по ссылке: ' \
                           'https://t.me/addstickers/'
                    await message.answer(text + url_pack,
                                         reply_markup=back_to_menu_keyboard)
            await asyncio.sleep(3)
