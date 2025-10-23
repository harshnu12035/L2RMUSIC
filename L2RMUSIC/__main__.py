import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from L2RMUSIC import LOGGER, app, userbot
from L2RMUSIC.core.call import Ashish
from L2RMUSIC.misc import sudo
from L2RMUSIC.plugins import ALL_MODULES
from L2RMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

async def init():
    # Check if required strings are set
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER.error("♦️ String session not filled, please fill a Pyrogram session 🍃...")
        exit()

    # Perform sudo actions
    await sudo()

    # Add banned users to the BANNED_USERS set
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER.error(f"Error while fetching banned users: {e}")

    # Start the Pyrogram app
    await app.start()

    # Dynamically load all modules
    for all_module in ALL_MODULES:
        try:
            importlib.import_module(f"L2RMUSIC.plugins.{all_module}")
        except ModuleNotFoundError as e:
            LOGGER.error(f"Failed to import module {all_module}: {e}")

    LOGGER.info("👻 All features loaded baby❣️...")

    # Start the userbot
    await userbot.start()

    # Start the Ashish voice call
    await Ashish.start()

    # Attempt to start streaming
    try:
        await Ashish.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER.error("🙏 Please start your log group voice chat/channel.\nMusic bot stopped ✨...")
        exit()
    except Exception as e:
        LOGGER.error(f"Error while starting stream: {e}")
    
    # Run decorators for Ashish
    await Ashish.decorators()

    LOGGER.info("╔═════ஜ۩۞۩ஜ════╗\n  ༄𝐿 2 𝙍.🖤🜲𝐾𝐼𝐍𝐺❦︎ 𝆺𝅥⃝🍷\n╚═════ஜ۩۞۩ஜ════╝")

    # Keep the bot running
    await idle()

    # Cleanly stop the app and userbot when done
    await app.stop()
    await userbot.stop()
    LOGGER.info("✨ Stopped L2R MUSIC bot 🎻🍒...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
