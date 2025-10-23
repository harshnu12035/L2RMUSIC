from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER  # Assuming you have a custom logger module


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
        # Start the bot
        await super().start()

        # Set bot info
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Send a startup message to the log group
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\n"
                     f"ɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Ensure that your bot is added."
            )
            raise SystemExit("Bot failed to access the log group/channel.")
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason: {type(ex).__name__}."
            )
            raise SystemExit(f"Bot failed to access the log group/channel. Reason: {type(ex).__name__}")

        # Ensure the bot is an admin in the log group/channel
        try:
            chat_member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot to an admin in your log group/channel."
                )
                raise SystemExit("Bot is not an admin in the log group/channel.")
        except Exception as ex:
            LOGGER(__name__).error(
                f"Error checking bot's admin status in the log group/channel.\n  Reason: {type(ex).__name__}"
            )
            raise SystemExit(f"Error checking admin status. Reason: {type(ex).__name__}")

        # Log bot startup
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        # Stop the bot cleanly
        await super().stop()
        LOGGER(__name__).info("Bot stopped successfully.")


if __name__ == "__main__":
    bot = Ashish()
    bot.run()  # Start the bot asynchronously
