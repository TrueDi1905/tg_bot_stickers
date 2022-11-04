import asyncio
import re

from pyrogram import Client
from sqlalchemy.orm import Session

from bot_tg import bot, dp
from models import engine, Users

#api_id = 25545663
#api_hash = "e16409f43cf6ea76437d10c1e7352596"

#app = Client("my_account", api_id=api_id, api_hash=api_hash)

#app.run()
#session = Session(bind=engine)
#user = Users(user_tg=9999999999)
#session.add(user)
#session.commit()

#app = Client("my_account")
#bot_active = False
#app.start()
#try:
#    app.get_me()
#except:
#    print(1)
#stickersbot.ddns.net