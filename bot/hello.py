import asyncio
from pyrogram import Client

api_id = 25545663
api_hash = "e16409f43cf6ea76437d10c1e7352596"


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())