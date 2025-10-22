from pyrogram import filters
from pyrogram.types import Message
from L2RMUSIC import app
from L2RMUSIC.misc import SUDOERS
from L2RMUSIC.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from L2RMUSIC.utils.decorators.language import language
from config import BANNED_USERS

@app.on_message(filters.command(["blchat", "blacklistchat"]) & SUDOERS)
@language
async def blacklist_chat_func(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_1"])

    try:
        chat_id = int(message.text.strip().split()[1])
    except (ValueError, IndexError):
        return await message.reply_text(_["black_1"])  # If chat_id is not valid

    # Check if the chat is already blacklisted
    if chat_id in await blacklisted_chats():
        return await message.reply_text(_["black_2"])

    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(_["black_3"])
    else:
        await message.reply_text(_["black_9"])

    # Attempt to make the bot leave the chat
    try:
        await app.leave_chat(chat_id)
    except Exception as e:
        # Log the error or handle it if needed
        print(f"Error leaving chat {chat_id}: {e}")
        pass

@app.on_message(filters.command(["whitelistchat", "unblacklistchat", "unblchat"]) & SUDOERS)
@language
async def whitelist_chat_func(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_4"])

    try:
        chat_id = int(message.text.strip().split()[1])
    except (ValueError,  IndexError):
        return await message.reply_text(_["black_4"])  # Invalid chat ID #aaoo

    # Check if chat is not in the blacklisted list
    if chat_id not in await blacklisted_chats():
        return await message.reply_text(_["black_5"])

    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(_["black_6"])
    
    await message.reply_text(_["black_9"])

@app.on_message(filters.command(["blchats", "blacklistedchats"]) & ~BANNED_USERS)
@language
async def all_blacklisted_chats(client, message: Message, _):
    text = _["black_7"]
    j = 0
    # Get all blacklisted chats
    blacklisted_chat_ids = await blacklisted_chats()

    if not blacklisted_chat_ids:
        return await message.reply_text(_["black_8"].format(app.mention))

    for count, chat_id in enumerate(blacklisted_chat_ids, 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception as e:
            # Handle private chats or inaccessible chats
            title = "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
            print(f"Error getting chat title for {chat_id}: {e}")
        
        text += f"{count}. {title} [<code>{chat_id}</code>]\n"
        j = 1  # Set j to 1 once we've added a blacklisted chat

    # If no chats, return a specific message
    if j == 0:
        await message.reply_text(_["black_8"].format(app.mention))
    else:
        await message.reply_text(text)
