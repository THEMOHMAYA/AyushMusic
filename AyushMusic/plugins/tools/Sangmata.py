import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from AyushMusic import userbot as us, app
from AyushMusic.core.userbot import assistants

@app.on_message(filters.command(["sg", "sangmata"]))
async def sg(client: Client, message: Message):
    if len(message.text.split()) < 2 and not message.reply_to_message:
        return await message.reply("<b>Usage:</b>\n/sg [Username/ID/Reply]")
    
    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1]
    
    lol = await message.reply("<code>Processing...</code>")
    
    try:
        user = await client.get_users(f"{args}")
    except Exception:
        return await lol.edit("<code>Please specify a valid user!</code>")
    
    bo = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(bo)
    
    # Check if assistant is available
    if not assistants:
        return await lol.edit("No Assistant found to process this request.")
    
    # Use assistant one
    ubot = us.one
    
    try:
        # Sending the ID to Sangmata Bot via Userbot
        a = await ubot.send_message(sg_bot, f"{user.id}")
    except Exception as e:
        return await lol.edit(f"Assistant Error: {e}")
    
    # Wait for the bot to reply
    await asyncio.sleep(3.5)
    
    found = False
    async for stalk in ubot.get_chat_history(sg_bot, limit=5):
        if stalk.from_user and stalk.from_user.username in bo:
            if stalk.text:
                await message.reply(f"{stalk.text}")
                found = True
                break
    
    if not found:
        await message.reply("Sangmata bot didn't respond. It might be down or slow.")
    
    # Clean up history in Sangmata Bot's chat
    try:
        user_info = await ubot.resolve_peer(sg_bot)
        await ubot.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass
    
    await lol.delete()
