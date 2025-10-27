import asyncio
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class Ashish(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="L2RMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        LOGGER(__name__).info("Attempting to connect to Telegram...")
        
        # --- FIX: Comprehensive Error Handling for Login (Including ValueError) ---
        while True:
            try:
                # This line attempts to connect and log in the bot
                await super().start()
                break  # If login is successful, break the loop
                
            except errors.FloodWait as e:
                wait_time = e.value
                LOGGER(__name__).warning(
                    f"⚠️ Telegram FloodWait during login. Waiting for {wait_time} seconds before retrying..."
                )
                await asyncio.sleep(wait_time)
                
            except (ValueError, errors.AuthKeyUnregistered, errors.BotMethodInvalid, errors.BadRequest) as ex:
                # This block specifically handles the ValueError and other fatal login errors.
                # ValueError often means an invalid or missing config variable (API_ID, BOT_TOKEN, etc.).
                LOGGER(__name__).error(
                    f"❌ Fatal Login Error! Check your BOT_TOKEN, API_ID, and API_HASH in config/Heroku Config Vars.\n  Reason: {type(ex).__name__} - {ex}"
                )
                # Application should exit if a fatal login error occurs as it cannot proceed.
                exit() 
                
            except Exception as ex:
                # Catch any other unexpected error during the start process
                LOGGER(__name__).error(
                    f"Bot failed to start due to an unexpected error: {type(ex).__name__} - {ex}"
                )
                exit()
        # --- END FIX ---
        
        # Login is successful, set bot info
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Logger/Log Channel Access Check (Original Code)
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            # Added a more specific log for the log channel error
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__} - {ex}."
            )
            exit()

        # Check for Admin status in log channel
        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
            
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
