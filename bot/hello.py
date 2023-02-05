import asyncio

from dotenv import dotenv_values
from pyrogram import Client


ENV = dotenv_values('../../.env')
api_id = ENV['API_ID']
api_hash = ENV['API_HASH']


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())
