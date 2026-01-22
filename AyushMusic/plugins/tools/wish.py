import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from AyushMusic import app

active_chats = {}

GM_MESSAGES = [
    "🌞 <b>Gᴏᴏᴅ Mᴏʀɴɪɴɢ</b> 🌼\n\n{mention}",
    "☕ <b>Rise and Shine!</b>\n\n{mention}",

    "🌞 <b>Sᴜʙᴀʜ Kɪ Sʜᴜʀᴜᴀᴀᴛ Mᴜsᴋᴀᴀɴ Sᴇ Kᴀʀᴏ</b>\n\n{mention}",
    "☀️ <b>Uᴛʜᴏ Aᴀᴊ Kᴜᴄʜ Aᴄʜʜᴀ Kᴀʀɴᴀ Hᴀɪ</b>\n\n{mention}",
    "🌄 <b>Sᴜʀᴀᴊ Kᴇ Sᴀᴀᴛʜ Nᴀʏɪ Uᴍᴍᴇᴇᴅᴇɴ</b>\n\n{mention}",
    "🌼 <b>Sᴜʙᴀʜ Aᴀʏɪ Hᴀɪ Kʜᴜsʜɪʏᴏɴ Kᴇ Sᴀᴀᴛʜ</b>\n\n{mention}",
    "💫 <b>Jᴀɢᴏ Aᴜʀ Aᴀᴊ Kᴏ Kʜᴀᴀs Bᴀɴᴀᴏ</b>\n\n{mention}",
    "🕊️ <b>Dɪʟ Mᴇɪɴ Sᴜᴋᴏᴏɴ, Cʜᴇʜʀᴇ Pᴇ Mᴜsᴋᴀᴀɴ</b>\n\n{mention}",
    "🌅 <b>Aᴀᴊ Kɪ Sᴜʙᴀʜ Kᴜᴄʜ Nᴀʏᴀ Lᴇᴋᴇ Aᴀʏɪ Hᴀɪ</b>\n\n{mention}",
    "🌸 <b>Sᴀᴘɴᴏɴ Kᴏ Aᴀᴊ Hᴀᴋɪᴋᴀᴛ Bᴀɴᴀᴏ</b>\n\n{mention}",
    "⭐ <b>Tᴜᴍʜᴀʀɪ Mᴜsᴋᴀᴀɴ Hɪ Sᴜʙᴀʜ Kɪ Rᴏsʜɴɪ Hᴀɪ</b>\n\n{mention}",
    "🌺 <b>Kʜᴜsʜ Rᴀʜᴏ, Kʜᴜsʜɪʏᴀɴ Bᴀᴀɴᴛᴏ</b>\n\n{mention}",
    "🦋 <b>Aᴀᴊ Kᴇ Dɪɴ Kᴏ Hᴀʟᴋᴀ Aᴜʀ Kʜᴜsʜɴᴜᴍᴀ Bᴀɴᴀᴏ</b>\n\n{mention}",
    "🌈 <b>Zɪɴᴅᴀɢɪ Kᴏ Aᴀᴊ Nᴀʏᴇ Rᴀɴɢ Dᴏ</b>\n\n{mention}",
    "🎶 <b>Sᴜʙᴀʜ Kɪ Hᴀᴡᴀ Aᴜʀ Sᴜᴋᴏᴏɴ Kɪ Bᴀᴀᴛᴇɴ</b>\n\n{mention}",
    "🌤️ <b>Uᴍᴍᴇᴇᴅᴏɴ Sᴇ Bʜᴀʀᴀ Yᴇʜ Sᴜʙᴀʜ</b>\n\n{mention}",
    "🌟 <b>Aᴀᴊ Kᴜᴄʜ Aᴄʜʜᴀ Hᴏɴᴇ Wᴀʟᴀ Hᴀɪ</b>\n\n{mention}",
    "💐 <b>Sᴀᴋᴀᴀʀᴀᴀᴛᴍᴀᴋ Sᴏᴄʜ Aᴜʀ Sᴜʙᴀʜ Kɪ Sʜᴜʙʜᴇᴄʜʜᴀ</b>\n\n{mention}"
]

GA_MESSAGES = [
    "🌞 <b>Gᴏᴏᴅ Aғᴛᴇʀɴᴏᴏɴ</b> ☀️\n\n{mention}",
"🍵 <b>Cʜᴀɪ Kᴀ Eᴋ Sɪᴘ, Dᴏᴘʜᴀʀ Kᴏ Sᴇᴛ Kᴀʀᴏ</b>\n\n{mention}",
    "🌤️ <b>Dʜᴜᴘ Mᴇɪɴ Bʜɪ Sᴜᴋᴏᴏɴ Dʜᴏᴏɴᴅʜ Lᴏ</b>\n\n{mention}",
    "😴 <b>Nɪɴᴅ Aᴀ Rᴀʜɪ Hᴀɪ? Tʜᴏᴅᴀ Sᴀ Bʀᴇᴀᴋ Lᴏ</b> 😜\n\n{mention}",
    "📣 <b>Hᴇʏ! Aᴀᴊ Kɪ Dᴏᴘʜᴀʀ Kʜᴀᴀs Hᴀɪ</b>\n\n{mention}",
    "☀️ <b>Dᴏᴘʜᴀʀ Kɪ Rᴏsʜɴɪ Aᴜʀ Nᴀʏɪ Tᴀᴋᴀᴛ</b>\n\n{mention}",
    "🥗 <b>Kʜᴀᴀɴᴀ Hᴏ Gᴀʏᴀ? Aʙ Tʜᴏᴅᴀ Aʀᴀᴀᴍ</b>\n\n{mention}",
    "💧 <b>Pᴀᴀɴɪ Pɪᴛᴇ Rᴀʜᴏ, Dʜᴜᴘ Tᴇᴢ Hᴀɪ</b>\n\n{mention}",
    "🌻 <b>Dᴏᴘʜᴀʀ Kᴏ Hᴀʟᴋᴀ Aᴜʀ Kʜᴜsʜʜᴀʟ Bᴀɴᴀᴏ</b>\n\n{mention}",
    "🍃 <b>Sᴀᴀɴs Lᴏ, Tʜᴏᴅᴀ Sᴀ Sᴜᴋᴏᴏɴ Pᴀᴀᴏ</b>\n\n{mention}",
    "🌸 <b>Lᴜɴᴄʜ Kᴇ Bᴀᴀᴅ Wᴀᴀʟɪ Mᴜsᴋᴀᴀɴ</b>\n\n{mention}",
    "🦋 <b>Dᴏᴘʜᴀʀ Bʜɪ Mᴀsᴛ Hᴏ Sᴀᴋᴛɪ Hᴀɪ</b>\n\n{mention}",
    "🍉 <b>Tʜᴀɴᴅᴀ Kʜᴀᴏ, Tʜᴀɴᴅᴀ Rᴀʜᴏ</b>\n\n{mention}",
    "🌺 <b>Dʜᴜᴘ Mᴇɪɴ Bʜɪ Kʜᴜsʜɪ Kᴀ Rᴀɴɢ</b>\n\n{mention}",
    "🎶 <b>Kᴀᴀᴍ Kᴇ Sᴀᴀᴛʜ Tʜᴏᴅɪ Sɪ Mᴜsɪᴄ</b>\n\n{mention}",
    "🌈 <b>Dᴏᴘʜᴀʀ Kᴏ Bʜɪ Rᴀɴɢɪɴ Bᴀɴᴀᴏ</b>\n\n{mention}"
]

GN_MESSAGES = [
    "🌙 <b>Gᴏᴏᴅ Nɪɢʜᴛ</b>\n\n{mention}",
    "💤 <b>Sᴏɴᴇ Cʜᴀʟᴏ, Kʜᴀᴡᴀʙᴏɴ Mᴇɪɴ Mɪʟᴛᴇ Hᴀɪɴ</b> 😴\n\n{mention}",
"🌌 <b>Rᴀᴀᴛ Kɪ Cʜᴜᴘᴘɪ Aᴜʀ Sᴜᴋᴏᴏɴ Tᴜᴍʜᴀʀᴇ Sᴀᴀᴛʜ</b>\n\n{mention}",
    "✨ <b>Hᴀʟᴋɪ Sɪ Rᴀᴀᴛ, Gᴇʜʀᴀ Aᴀʀᴀᴀᴍ</b>\n\n{mention}",
    "🌃 <b>Dɪɴ Bʜᴀʀ Kᴇ Bᴀᴀᴅ Aʙ Aᴀʀᴀᴀᴍ Kᴀ Wᴀǫᴛ</b>\n\n{mention}",
    "🌟 <b>Sɪᴛᴀʀᴇ Gɪɴᴛᴇ Gɪɴᴛᴇ Sᴏ Jᴀᴏ</b>\n\n{mention}",
    "🌙 <b>Cʜᴀᴀɴᴅ Kɪ Tʜᴀɴᴅɪ Rᴏsʜɴɪ Mᴇɪɴ Kʜᴏ Jᴀᴏ</b>\n\n{mention}",
    "🕊️ <b>Dɪʟ Kᴏ Sᴜᴋᴏᴏɴ, Aᴀɴᴋʜᴏɴ Kᴏ Nɪɴᴅ</b>\n\n{mention}",
    "🎭 <b>Sᴀᴘɴᴏɴ Kᴇ Sᴀᴀᴛʜ Eᴋ Nᴀʏɪ Dᴜɴɪʏᴀ</b>\n\n{mention}",
    "💫 <b>Rᴀᴀᴛ Kᴀ Jᴀᴀᴅᴜ Aʙ Sᴜʀᴜ Hᴏɴᴇ Dᴏ</b>\n\n{mention}",
    "🎵 <b>Hᴀʟᴋɪ Sɪ Lᴏʀɪ, Aᴜʀ Mᴇᴇᴛʜᴇ Sᴀᴘɴᴇ</b>\n\n{mention}",
    "🌸 <b>Aᴀᴊ Kᴇ Sᴀᴀʀᴇ Fɪᴋʀ Cʜʜᴏʀᴋᴇ Sᴏ Jᴀᴏ</b>\n\n{mention}",
    "🦋 <b>Kʜᴀᴀʙᴏɴ Mᴇɪɴ Uᴅᴀᴀɴ Bʜᴀʀᴏ</b>\n\n{mention}",
    "🌈 <b>Sᴀᴘɴᴏɴ Kᴏ Rᴀɴɢɪɴ Bᴀɴᴀᴏ</b>\n\n{mention}",
    "🕯️ <b>Rᴀᴀᴛ Kɪ Sʜᴀᴀɴᴛɪ Mᴇɪɴ Kʜᴜᴅ Sᴇ Mɪʟᴏ</b>\n\n{mention}",
    "🌅 <b>Aᴀᴊ Kᴏ Yᴀʜɪɴ Cʜʜᴏʀᴏ, Kᴀʟ Pʜɪʀ Mɪʟᴇɴɢᴇ</b>\n\n{mention}",
    "😴 <b>Aᴀɴᴋʜᴇɪɴ Bᴀɴᴅ, Sᴜᴋᴏᴏɴ Bᴇʜɪsᴀᴀʙ</b>\n\n{mention}"
]

async def get_chat_users(chat_id):
    """Get all valid users from a chat (excluding bots and deleted accounts)"""
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    return users

async def tag_users(chat_id, messages, tag_type):
    """Generic function to tag users one by one with specified messages"""
    users = await get_chat_users(chat_id)
    
    for user in users:
        # Check if tagging was stopped
        if chat_id not in active_chats:
            break
            
        mention = f"<b><a href='tg://user?id={user.id}'>{user.first_name}</a></b>"
        msg = random.choice(messages).format(mention=mention)
        
        await app.send_message(chat_id, msg, disable_web_page_preview=True)
        await asyncio.sleep(3)
    
    active_chats.pop(chat_id, None)
    await app.send_message(chat_id, f"✅ <b>{tag_type} Tᴀɢɢɪɴɢ Dᴏɴᴇ!</b>")


@app.on_message(filters.command("gmtag") & filters.group)
async def gmtag(_, message: Message):
    """Start Good Morning tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ <b>Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Rᴜɴɴɪɴɢ.</b>")
    
    active_chats[chat_id] = True
    await message.reply("☀️ <b>Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...</b>")
    
    await tag_users(chat_id, GM_MESSAGES, "Gᴏᴏᴅ Mᴏʀɴɪɴɢ")

@app.on_message(filters.command("gmstop") & filters.group)
async def gmstop(_, message: Message):
    """Stop Good Morning tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 <b>Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.</b>")
    else:
        await message.reply("❌ <b>Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.</b>")


@app.on_message(filters.command("gatag") & filters.group)
async def gatag(_, message: Message):
    """Start Good Afternoon tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ <b>Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Oɴ.</b>")
    
    active_chats[chat_id] = True
    await message.reply("☀️ <b>Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...</b>")
    
    await tag_users(chat_id, GA_MESSAGES, "Aғᴛᴇʀɴᴏᴏɴ")

@app.on_message(filters.command("gastop") & filters.group)
async def gastop(_, message: Message):
    """Stop Good Afternoon tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 <b>Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.</b>")
    else:
        await message.reply("❌ <b>Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.</b>")


@app.on_message(filters.command("gntag") & filters.group)
async def gntag(_, message: Message):
    """Start Good Night tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ <b>Nɪɢʜᴛ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Oɴ.</b>")
    
    active_chats[chat_id] = True
    await message.reply("🌙 <b>Nɪɢʜᴛ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...</b>")
    
    await tag_users(chat_id, GN_MESSAGES, "Gᴏᴏᴅ Nɪɢʜᴛ")

@app.on_message(filters.command("gnstop") & filters.group)
async def gnstop(_, message: Message):
    """Stop Good Night tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 <b>Nɪɢʜᴛ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.</b>")
    else:
        await message.reply("❌ <b>Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.</b>")


@app.on_message(filters.command("stopall") & filters.group)
async def stopall(_, message: Message):
    """Stop all active tagging in current chat"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 <b>Aʟʟ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.</b>")
    else:
        await message.reply("❌ <b>Nᴏ Aᴄᴛɪᴠᴇ Tᴀɢɢɪɴɢ Fᴏᴜɴᴅ.</b>")

@app.on_message(filters.command("taghelp") & filters.group)
async def taghelp(_, message: Message):
    """Show help message for tagging commands"""
    help_text = """
🏷️ <b>Tagging Commands Help</b>

<b>Good Morning:</b>
• <code>/gmtag</code> - Start Good Morning tagging
• <code>/gmstop</code> - Stop Good Morning tagging

<b>Good Afternoon:</b>
• <code>/gatag</code> - Start Good Afternoon tagging  
• <code>/gastop</code> - Stop Good Afternoon tagging

<b>Good Night:</b>
• <code>/gntag</code> - Start Good Night tagging
• <code>/gnstop</code> - Stop Good Night tagging

<b>Utility:</b>
• <code>/stopall</code> - Stop all active tagging
• <code>/taghelp</code> - Show this help message

<b>Note:</b> Now tags one user at a time with 3 second delay between each user. Only one tagging session can run per chat at a time.
"""
    await message.reply(help_text)


