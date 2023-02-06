import asyncio


from pyrogram import Client
from sqlalchemy.orm import Session
from sqlalchemy import select, update, values
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
                if pack_option == '/addsticker':
                    await app.send_message("@Stickers", pack_option)
                    await app.send_message("@Stickers", f'{message.text}')
                    await app.send_document("@Stickers", photo)
                    smile_id = session.execute(
                        select([Stickers.smile_id]).where(Stickers.stickers_tg == message.text)).fetchone()[0]
                    if smile_id == 120:
                        await message.answer('В этот пак больше стикеров добавить нельзя(, создай новый',
                                             reply_markup=back_to_menu_keyboard)

                        return
                    await app.send_message("@Stickers", send_smile(smile_id))
                    session.execute(update(Stickers).where(
                        Stickers.stickers_tg == message.text).values(
                        smile_id=smile_id + 1))
                    session.commit()
                    
                if pack_option == '/newpack':
                    await app.send_message("@Stickers", pack_option)
                    await app.send_message("@Stickers", f'{message.text} @Stickers_Now_Bot')
                    get_user = len(engine.execute(
                        select(Users).where(Users.user_tg == message.from_user.id)).fetchall())
                    if get_user == 0:
                        user = Users(user_tg=message.from_user.id)
                        session.add(user)
                        session.commit()
                    smile_id = 0
                    await app.send_document("@Stickers", photo)
                    await app.send_message("@Stickers", send_smile(smile_id))
                    await asyncio.sleep(1)
                    await app.send_message("@Stickers", '/publish')
                    await app.send_message("@Stickers", '/skip')
                    get_stickers = len(engine.execute(
                        select(Stickers.id)).fetchall())
                    url_pack = f'Stickers_Now_Bot_pack_{get_stickers + 1}'
                    await app.send_message("@Stickers", url_pack)
                    sticker = Stickers(stickers_tg=url_pack,
                                       tg_users=message.from_user.id,
                                       smile_id=smile_id)
                    session.add(sticker)
                    session.commit()
                    text = 'Ваш набор доступен по ссылке: ' \
                           'https://t.me/addstickers/'
                    await message.answer(text + url_pack,
                                         reply_markup=back_to_menu_keyboard)
            await asyncio.sleep(3)
