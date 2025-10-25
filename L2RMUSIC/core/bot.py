from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER  # Your custom logger


class Ashish(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
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
        """Start the bot safely"""
        await super().start()

        # Basic bot info
        self.id = self.me.id
        self.name = f"{self.me.first_name or ''} {self.me.last_name or ''}".strip()
        self.username = self.me.username or "Unknown"
        self.mention = self.me.mention

        LOGGER(__name__).info(f"Bot logged in as {self.name} (@{self.username})")

        # Validate LOGGER_ID format
        if not str(config.LOGGER_ID).startswith("-100"):
            LOGGER(__name__).error(
                f"Invalid LOGGER_ID: {config.LOGGER_ID}. Must start with -100 for channels/supergroups."
            )
            raise SystemExit("❌ Invalid LOGGER_ID format. It must start with -100.")

        # Attempt to send startup message
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )
            LOGGER(__name__).info("Startup message sent successfully.")
        except errors.PeerIdInvalid:
            LOGGER(__name__).error(
                f"PeerIdInvalid: LOGGER_ID {config.LOGGER_ID} not found. "
                "Ensure the bot is in that group/channel."
            )
            raise SystemExit("❌ Invalid LOGGER_ID. Bot not in that chat.")
        except errors.ChannelInvalid:
            LOGGER(__name__).error(
                f"ChannelInvalid: LOGGER_ID {config.LOGGER_ID} is incorrect or inaccessible."
            )
            raise SystemExit("❌ Bot cannot access the log channel/group.")
        except errors.ChatWriteForbidden:
            LOGGER(__name__).error("Bot cannot send messages in the log chat. Needs permission.")
            raise SystemExit("❌ Bot cannot send messages in log group/channel.")
        except Exception as ex:
            LOGGER(__name__).error(f"Unexpected error sending log message: {type(ex).__name__} - {ex}")
            raise SystemExit(f"❌ Unexpected startup error: {type(ex).__name__}")

        # Check admin rights in log chat
        try:
            chat_member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Bot is not admin in the log group/channel. Promote it first."
                )
                raise SystemExit("❌ Bot must be admin in the log group/channel.")
        except errors.UserNotParticipant:
            LOGGER(__name__).error("Bot is not a participant in the log group/channel.")
            raise SystemExit("❌ Bot not added to log group/channel.")
        except Exception as ex:
            LOGGER(__name__).error(
                f"Error checking admin status in log chat: {type(ex).__name__} - {ex}"
            )
            raise SystemExit(f"❌ Error checking admin status: {type(ex).__name__}")

        LOGGER(__name__).info(f"✅ Music Bot Started Successfully as {self.name}")

    async def stop(self):
        """Gracefully stop the bot"""
        await super().stop()
        LOGGER(__name__).info("Bot stopped successfully.")


if __name__ == "__main__":
    bot = Ashish()
    bot.run()
