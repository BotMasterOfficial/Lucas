# credits @mkspali

import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Lucas import DRAGONS as SUDO_USERS
from Lucas import pbot
from Lucas.modules.sql_extended import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ 𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 @{channel} 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐚𝐧𝐝 𝐩𝐫𝐞𝐬𝐬 '𝐔𝐧𝐌𝐮𝐭𝐞 𝐌𝐞' 𝐛𝐮𝐭𝐭𝐨𝐧.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐦𝐮𝐭𝐞𝐝 𝐛𝐲 𝐚𝐝𝐦𝐢𝐧𝐬 𝐝𝐮𝐞 𝐭𝐨 𝐬𝐨𝐦𝐞 𝐨𝐭𝐡𝐞𝐫 𝐫𝐞𝐚𝐬𝐨𝐧.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} 𝐢𝐬 𝐭𝐫𝐲𝐢𝐧𝐠 𝐭𝐨 𝐔𝐧𝐌𝐮𝐭𝐞 𝐡𝐢𝐦𝐬𝐞𝐥𝐟 𝐛𝐮𝐭 𝐢 𝐜𝐚𝐧'𝐭 𝐮𝐧𝐦𝐮𝐭𝐞 𝐡𝐢𝐦 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐢 𝐚𝐦 𝐧𝐨𝐭 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭 𝐚𝐝𝐝 𝐦𝐞 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧 𝐚𝐠𝐚𝐢𝐧.**\n__#𝐋𝐞𝐚𝐯𝐢𝐧𝐠 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ 𝐖𝐚𝐫𝐧𝐢𝐧𝐠! 𝐃𝐨𝐧'𝐭 𝐩𝐫𝐞𝐬𝐬 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐰𝐡𝐞𝐧 𝐲𝐨𝐮 𝐜𝐚𝐧 𝐭𝐚𝐥𝐤.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {} 🙏 \n **𝐘𝐨𝐮 𝐡𝐚𝐯𝐞𝐧'𝐭 𝐣𝐨𝐢𝐧𝐞𝐝 𝐨𝐮𝐫 @{} 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐲𝐞𝐭** 😭 \n \n𝐏𝐥𝐞𝐚𝐬𝐞 𝐉𝐨𝐢𝐧 [𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/{}) 𝐚𝐧𝐝 𝐡𝐢𝐭 𝐭𝐡𝐞 **𝐔𝐍𝐌𝐔𝐓𝐄 𝐌𝐄** 𝐁𝐮𝐭𝐭𝐨𝐧. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "🔰𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥🔰",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "🔊𝐔𝐧𝐌𝐮𝐭𝐞 𝐌𝐞🔊", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **𝐋𝐮𝐜𝐚𝐬 𝐢𝐬 𝐧𝐨𝐭 𝐚𝐝𝐦𝐢𝐧 𝐡𝐞𝐫𝐞..**\n__𝐆𝐢𝐯𝐞 𝐦𝐞 𝐛𝐚𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐚𝐧𝐝 𝐫𝐞𝐭𝐫𝐲..\n#𝐄𝐧𝐝𝐢𝐧𝐠 𝐅𝐒𝐮𝐛...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"❗ **𝐈 𝐧𝐨𝐭 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐨𝐟 @{channel} 𝐜𝐡𝐚𝐧𝐧𝐞𝐥.**\n__𝐆𝐢𝐯𝐞 𝐦𝐞 𝐚𝐝𝐦𝐢𝐧 𝐨𝐟 𝐭𝐡𝐚𝐭 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐚𝐧𝐝 𝐫𝐞𝐭𝐫𝐲.\n#𝐄𝐧𝐝𝐢𝐧𝐠 𝐅𝐒𝐮𝐛...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐢𝐬 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**𝐔𝐧𝐦𝐮𝐭𝐢𝐧𝐠 𝐚𝐥𝐥 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐰𝐡𝐨 𝐚𝐫𝐞 𝐦𝐮𝐭𝐞𝐝 𝐛𝐲 𝐦𝐞...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **𝐔𝐧𝐌𝐮𝐭𝐞𝐝 𝐚𝐥𝐥 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐰𝐡𝐨 𝐚𝐫𝐞 𝐦𝐮𝐭𝐞𝐝 𝐛𝐲 𝐦𝐞.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **𝐈 𝐚𝐦 𝐧𝐨𝐭 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.**\n__𝐈 𝐜𝐚𝐧'𝐭 𝐮𝐧𝐦𝐮𝐭𝐞 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐈 𝐚𝐦 𝐧𝐨𝐭 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭 𝐦𝐚𝐤𝐞 𝐦𝐞 𝐚𝐝𝐦𝐢𝐧 𝐰𝐢𝐭𝐡 𝐛𝐚𝐧 𝐮𝐬𝐞𝐫 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐢𝐬 𝐄𝐧𝐚𝐛𝐥𝐞𝐝**\n__𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐢𝐬 𝐞𝐧𝐚𝐛𝐥𝐞𝐝, 𝐚𝐥𝐥 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐡𝐚𝐯𝐞 𝐭𝐨 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐭𝐡𝐢𝐬 [𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/{input_str}) 𝐢𝐧 𝐨𝐫𝐝𝐞𝐫 𝐭𝐨 𝐬𝐞𝐧𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐠𝐫𝐨𝐮𝐩.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **𝐍𝐨𝐭 𝐚𝐧 𝐀𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥**\n__𝐈 𝐚𝐦 𝐧𝐨𝐭 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐞 [𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/{input_str}). 𝐀𝐝𝐝 𝐦𝐞 𝐚𝐬 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐨𝐫𝐝𝐞𝐫 𝐭𝐨 𝐞𝐧𝐚𝐛𝐥𝐞 𝐅𝐨𝐫𝐜𝐞𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞.**")
                except Exception as err:
                    message.reply_text(f"❗ **𝐄𝐑𝐑𝐎𝐑:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐢𝐬 𝐞𝐧𝐚𝐛𝐥𝐞𝐝 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.**\n__𝐅𝐨𝐫 𝐭𝐡𝐢𝐬 [𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞 𝐢𝐬 𝐝𝐢𝐬𝐚𝐛𝐥𝐞𝐝 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.**")
    else:
        message.reply_text(
            "❗ **𝐆𝐫𝐨𝐮𝐩 𝐂𝐫𝐞𝐚𝐭𝐨𝐫 𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝**\n__𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐭𝐨 𝐛𝐞 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐜𝐫𝐞𝐚𝐭𝐨𝐫 𝐭𝐨 𝐝𝐨 𝐭𝐡𝐚𝐭.__"
        )


__help__ = """
*𝐅𝐨𝐫𝐜𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞:*
⚫ 𝐋𝐮𝐜𝐚𝐬 𝐜𝐚𝐧 𝐦𝐮𝐭𝐞 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐰𝐡𝐨 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐝 𝐲𝐨𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐮𝐧𝐭𝐢𝐥 𝐭𝐡𝐞𝐲 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞
⚫ 𝐖𝐡𝐞𝐧 𝐞𝐧𝐚𝐛𝐥𝐞𝐝 𝐈 𝐰𝐢𝐥𝐥 𝐦𝐮𝐭𝐞 𝐮𝐧𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐝 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐚𝐧𝐝 𝐬𝐡𝐨𝐰 𝐭𝐡𝐞𝐦 𝐚 𝐮𝐧𝐦𝐮𝐭𝐞 𝐛𝐮𝐭𝐭𝐨𝐧. 𝐖𝐡𝐞𝐧 𝐭𝐡𝐞𝐲 𝐩𝐫𝐞𝐬𝐬𝐞𝐝 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐈 𝐰𝐢𝐥𝐥 𝐮𝐧𝐦𝐮𝐭𝐞 𝐭𝐡𝐞𝐦
*𝐒𝐞𝐭𝐮𝐩*
*𝐎𝐧𝐥𝐲 𝐜𝐫𝐞𝐚𝐭𝐨𝐫*
⚫ 𝐀𝐝𝐝 𝐦𝐞 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧
⚫ 𝐀𝐝𝐝 𝐦𝐞 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧
 
*𝐂𝐨𝐦𝐦𝐦𝐚𝐧𝐝𝐬*
 ⚫ /fsub {Channel Username} - 𝐓𝐨 𝐭𝐮𝐫𝐧 𝐨𝐧 𝐚𝐧𝐝 𝐬𝐞𝐭𝐮𝐩 𝐭𝐡𝐞 𝐜𝐡𝐚𝐧𝐧𝐞𝐥.
  💡𝐃𝐨 𝐭𝐡𝐢𝐬 𝐟𝐢𝐫𝐬𝐭...
 ⚫ /fsub - 𝐓𝐨 𝐠𝐞𝐭 𝐭𝐡𝐞 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬.
 ⚫ /fusb disable - 𝐓𝐨 𝐭𝐮𝐫𝐧 𝐨𝐟 𝐅𝐨𝐫𝐜𝐞𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞..
  💡𝐈𝐟 𝐲𝐨𝐮 𝐝𝐢𝐬𝐚𝐛𝐥𝐞 𝐟𝐬𝐮𝐛, 𝐲𝐨𝐮 𝐧𝐞𝐞𝐝 𝐭𝐨 𝐬𝐞𝐭 𝐚𝐠𝐚𝐢𝐧 𝐟𝐨𝐫 𝐰𝐨𝐫𝐤𝐢𝐧𝐠.. 
    /fsub {Channel Username} 
 ⚫ /fsub clear - 𝐓𝐨 𝐮𝐧𝐦𝐮𝐭𝐞 𝐚𝐥𝐥 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐰𝐡𝐨 𝐦𝐮𝐭𝐞𝐝 𝐛𝐲 𝐦𝐞.
"""
__mod_name__ = "♾️𝐅-𝐒𝐮𝐛♾️"
