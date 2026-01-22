import logging

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid


@Client.on_message(filters.command("banall") & filters.group)
async def banall_command(client: Client, message: Message):
    if not message.from_user:
        return

    # check admin
    try:
        admins = [
            admin.user.id async for admin in client.get_chat_members(
                message.chat.id,
                filter=ChatMembersFilter.ADMINISTRATORS
            )
        ]
    except ChatAdminRequired:
        await message.reply("❌ ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴅᴍɪɴs!")
        return

    if message.from_user.id not in admins:
        await message.reply("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!")
        return

    status = await message.reply("⚡ sᴛᴀʀᴛɪɴɢ ʙᴀɴᴀʟʟ ᴘʀᴏᴄᴇss...")

    banned = 0

    async for member in client.get_chat_members(message.chat.id):
        try:
            if (
                member.user.is_bot
                or member.user.id in admins
                or member.user.is_deleted
            ):
                continue

            await client.ban_chat_member(
                chat_id=message.chat.id,
                user_id=member.user.id
            )
            banned += 1
            logging.info(f"banned {member.user.id} from {message.chat.id}")

        except ChatAdminRequired:
            await status.edit("⚠️ ɪ ɴᴇᴇᴅ ʙᴀɴ ᴍᴇᴍʙᴇʀs ᴘᴇʀᴍɪssɪᴏɴ!")
            return

        except PeerIdInvalid:
            continue

        except Exception as e:
            logging.warning(f"failed to ban {member.user.id}: {e}")

    await status.edit(
        f"✅ ʙᴀɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!\n\n"
        f"🔨 ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ: `{banned}`"
    )