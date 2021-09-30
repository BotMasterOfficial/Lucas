#    Copyright (C) @BotMasterOfficial 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio
import os
import re

import better_profanity
import emoji
import nude
import requests
from better_profanity import profanity
from google_trans_new import google_translator
from telethon import events
from telethon.tl.types import ChatBannedRights

from Lucas import BOT_ID
from Lucas.conf import get_int_key, get_str_key

# from Lucas.db.mongo_helpers.nsfw_guard import add_chat, get_all_nsfw_chats, is_chat_in_db, rm_chat
from Lucas.pyrogramee.telethonbasics import is_admin
from Lucas.events import register
from Lucas import MONGO_DB_URI 
from pymongo import MongoClient
from Lucas.modules.sql_extended.nsfw_watch_sql import (
    add_nsfwatch,
    get_all_nsfw_enabled_chat,
    is_nsfwatch_indb,
    rmnsfwatch,
)
from Lucas import telethn as tbot

translator = google_translator()
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

MONGO_DB_URI = get_str_key("MONGO_DB_URI")

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Lucas"]

async def is_nsfw(event):
    lmao = event
    if not (
        lmao.gif
        or lmao.video
        or lmao.video_note
        or lmao.photo
        or lmao.sticker
        or lmao.media
    ):
        return False
    if lmao.video or lmao.video_note or lmao.sticker or lmao.gif:
        try:
            starkstark = await event.client.download_media(lmao.media, thumb=-1)
        except:
            return False
    elif lmao.photo or lmao.sticker:
        try:
            starkstark = await event.client.download_media(lmao.media)
        except:
            return False
    img = starkstark
    f = {"file": (img, open(img, "rb"))}

    r = requests.post("https://starkapi.herokuapp.com/nsfw/", files=f).json()
    if r.get("success") is False:
        is_nsfw = False
    elif r.get("is_nsfw") is True:
        is_nsfw = True
    elif r.get("is_nsfw") is False:
        is_nsfw = False
    return is_nsfw


@tbot.on(events.NewMessage(pattern="/gshield (.*)"))
async def nsfw_watch(event):
    if not event.is_group:
        await event.reply("𝐘𝐨𝐮 𝐂𝐚𝐧 𝐎𝐧𝐥𝐲 𝐍𝐬𝐟𝐰 𝐖𝐚𝐭𝐜𝐡 𝐢𝐧 𝐆𝐫𝐨𝐮𝐩𝐬.")
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`𝐈 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return
    if await is_admin(event, event.message.sender_id):
        if (
            input_str == "on"
            or input_str == "On"
            or input_str == "ON"
            or input_str == "enable"
        ):
            if is_nsfwatch_indb(str(event.chat_id)):
                await event.reply("`𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐇𝐚𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 𝐍𝐬𝐟𝐰 𝐖𝐚𝐭𝐜𝐡.`")
                return
            add_nsfwatch(str(event.chat_id))
            await event.reply(
                f"**𝐀𝐝𝐝𝐞𝐝 𝐂𝐡𝐚𝐭 {event.chat.title} 𝐖𝐢𝐭𝐡 𝐈𝐝 {event.chat_id} 𝐓𝐨 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞. 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩𝐬 𝐍𝐬𝐟𝐰 𝐂𝐨𝐧𝐭𝐞𝐧𝐭𝐬 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐃𝐞𝐥𝐞𝐭𝐞𝐝**"
            )
        elif (
            input_str == "off"
            or input_str == "Off"
            or input_str == "OFF"
            or input_str == "disable"
        ):
            if not is_nsfwatch_indb(str(event.chat_id)):
                await event.reply("𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐇𝐚𝐬 𝐍𝐨𝐭 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 𝐍𝐬𝐟𝐰 𝐖𝐚𝐭𝐜𝐡.")
                return
            rmnsfwatch(str(event.chat_id))
            await event.reply(
                f"**𝐑𝐞𝐦𝐨𝐯𝐞𝐝 𝐂𝐡𝐚𝐭 {event.chat.title} 𝐖𝐢𝐭𝐡 𝐈𝐝 {event.chat_id} 𝐅𝐫𝐨𝐦 𝐍𝐬𝐟𝐰 𝐖𝐚𝐭𝐜𝐡**"
            )
        else:
            await event.reply(
                "𝐈 𝐮𝐧𝐝𝐞𝐬𝐭𝐚𝐧𝐝 `/𝐧𝐬𝐟𝐰𝐠𝐮𝐚𝐫𝐝𝐢𝐚𝐧 𝐨𝐧` 𝐚𝐧𝐝 `/𝐧𝐬𝐟𝐰𝐠𝐮𝐚𝐫𝐝𝐢𝐚𝐧 𝐨𝐟𝐟` 𝐨𝐧𝐥𝐲"
            )
    else:
        await event.reply("`𝐘𝐨𝐮 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return


@tbot.on(events.NewMessage())
async def ws(event):
    warner_starkz = get_all_nsfw_enabled_chat()
    if len(warner_starkz) == 0:
        return
    if not is_nsfwatch_indb(str(event.chat_id)):
        return
    if not (event.photo):
        return
    if not await is_admin(event, BOT_ID):
        return
    if await is_admin(event, event.message.sender_id):
        return
    sender = await event.get_sender()
    await event.client.download_media(event.photo, "nudes.jpg")
    if nude.is_nude("./nudes.jpg"):
        await event.delete()
        st = sender.first_name
        hh = sender.id
        final = f"**NSFW DETECTED**\n\n{st}](tg://user?id={hh}) your message contain NSFW content.. So, Lucas deleted the message\n\n **Nsfw Sender - User / Bot :** {st}](tg://user?id={hh})  \n\n`⚔️Automatic Detections Powered By LucasAI` \n**#GROUP_GUARDIAN** "
        dev = await event.respond(final)
        await asyncio.sleep(10)
        await dev.delete()
        os.remove("nudes.jpg")


"""
@pbot.on_message(filters.command("nsfwguardian") & ~filters.edited & ~filters.bot)
async def add_nsfw(client, message):
    if len(await member_permissions(message.chat.id, message.from_user.id)) < 1:
        await message.reply_text("**𝐘𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐞𝐧𝐨𝐮𝐠𝐡 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬**")
        return
    status = message.text.split(None, 1)[1] 
    if status == "on" or status == "ON" or status == "enable":
        pablo = await message.reply("`𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠...`")
        if is_chat_in_db(message.chat.id):
            await pablo.edit("𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐢𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐈𝐧 𝐌𝐲 𝐃𝐁")
            return
        me = await client.get_me()
        add_chat(message.chat.id)
        await pablo.edit("𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐀𝐝𝐝𝐞𝐝 𝐂𝐡𝐚𝐭 𝐓𝐨 𝐍𝐒𝐅𝐖 𝐖𝐚𝐭𝐜𝐡.")
        
    elif status == "off" or status=="OFF" or status == "disable":
        pablo = await message.reply("`𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠...`")
        if not is_chat_in_db(message.chat.id):
            await pablo.edit("𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐢𝐬 𝐍𝐨𝐭 𝐢𝐧 𝐃𝐁.")
            return
        rm_chat(message.chat.id)
        await pablo.edit("𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐑𝐞𝐦𝐨𝐯𝐞𝐝 𝐂𝐡𝐚𝐭 𝐅𝐫𝐨𝐦 𝐍𝐒𝐅𝐖 𝐖𝐚𝐭𝐜𝐡 𝐬𝐞𝐫𝐯𝐢𝐜𝐞")
    else:
        await message.reply(" 𝐈 𝐮𝐧𝐝𝐞𝐬𝐭𝐚𝐧𝐝 𝐨𝐧𝐥𝐲 `/𝐧𝐬𝐟𝐰𝐠𝐮𝐚𝐫𝐝𝐢𝐚𝐧 𝐨𝐧` 𝐨𝐫 `/𝐧𝐬𝐟𝐰𝐠𝐮𝐚𝐫𝐝𝐢𝐚𝐧 𝐨𝐟𝐟` 𝐨𝐧𝐥𝐲")
        
@pbot.on_message(filters.incoming & filters.media & ~filters.private & ~filters.channel & ~filters.bot)
async def nsfw_watch(client, message):
    lol = get_all_nsfw_chats()
    if len(lol) == 0:
        message.continue_propagation()
    if not is_chat_in_db(message.chat.id):
        message.continue_propagation()
    hot = await is_nsfw(client, message)
    if not hot:
        message.continue_propagation()
    else:
        try:
            await message.delete()
        except:
            pass
        lolchat = await client.get_chat(message.chat.id)
        ctitle = lolchat.title
        if lolchat.username:
            hehe = lolchat.username
        else:
            hehe = message.chat.id
        midhun = await client.get_users(message.from_user.id)
        await message.delete()
        if midhun.username:
            Escobar = midhun.username
        else:
            Escobar = midhun.id
        await client.send_message(
            message.chat.id,
            f"**NSFW DETECTED**\n\n{hehe}'s message contain NSFW content.. So, Lucas deleted the message\n\n **Nsfw Sender - User / Bot :** `{Escobar}` \n**Chat Title:** `{ctitle}` \n\n`⚔️Automatic Detections Powered By LucasAI` \n**#GROUP_GUARDIAN** ",
        )
        message.continue_propagation()
"""


# This Module is ported from https://github.com/BotMasterOfficial/Lucas
# This hardwork was completely done by Lucas
# Full Credits goes to Lucas


approved_users = db.approve
spammers = db.spammer
globalchat = db.globchat

CMD_STARTERS = "/"
profanity.load_censor_words_from_file("./profanity_wordlist.txt")


@register(pattern="^/profanity(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("𝐘𝐨𝐮 𝐂𝐚𝐧 𝐎𝐧𝐥𝐲 𝐩𝐫𝐨𝐟𝐚𝐧𝐢𝐭𝐲 𝐢𝐧 𝐆𝐫𝐨𝐮𝐩𝐬.")
        return
    event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`𝐈 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return
    if await is_admin(event, event.message.sender_id):
        input = event.pattern_match.group(1)
        chats = spammers.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐬𝐨𝐦𝐞 𝐢𝐧𝐩𝐮𝐭 𝐲𝐞𝐬 𝐨𝐫 𝐧𝐨.\𝐧\𝐧𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐢𝐬 : **𝐨𝐧**"
                    )
                    return
            await event.reply(
                "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐬𝐨𝐦𝐞 𝐢𝐧𝐩𝐮𝐭 𝐲𝐞𝐬 𝐨𝐫 𝐧𝐨.\𝐧\𝐧𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐢𝐬 : **𝐨𝐟𝐟**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply(
                            "𝐏𝐫𝐨𝐟𝐚𝐧𝐢𝐭𝐲 𝐟𝐢𝐥𝐭𝐞𝐫 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭."
                        )
                        return
                spammers.insert_one({"id": event.chat_id})
                await event.reply("𝐏𝐫𝐨𝐟𝐚𝐧𝐢𝐭𝐲 𝐟𝐢𝐥𝐭𝐞𝐫 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐧 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
        if input == "off":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        spammers.delete_one({"id": event.chat_id})
                        await event.reply("𝐏𝐫𝐨𝐟𝐚𝐧𝐢𝐭𝐲 𝐟𝐢𝐥𝐭𝐞𝐫 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐟𝐟 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
                        return
            await event.reply("𝐏𝐫𝐨𝐟𝐚𝐧𝐢𝐭𝐲 𝐟𝐢𝐥𝐭𝐞𝐫 𝐢𝐬𝐧'𝐭 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐧 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
        if not input == "on" and not input == "off":
            await event.reply("𝐈 𝐨𝐧𝐥𝐲 𝐮𝐧𝐝𝐞𝐫𝐬𝐭𝐚𝐧𝐝 𝐛𝐲 𝐨𝐧 𝐨𝐫 𝐨𝐟𝐟")
            return
    else:
        await event.reply("`𝐘𝐨𝐮 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return


@register(pattern="^/globalmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("𝐘𝐨𝐮 𝐂𝐚𝐧 𝐎𝐧𝐥𝐲 𝐞𝐧𝐚𝐛𝐥𝐞 𝐠𝐥𝐨𝐛𝐚𝐥 𝐦𝐨𝐝𝐞 𝐖𝐚𝐭𝐜𝐡 𝐢𝐧 𝐆𝐫𝐨𝐮𝐩𝐬.")
        return
    event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`𝐈 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return
    if await is_admin(event, event.message.sender_id):

        input = event.pattern_match.group(1)
        chats = globalchat.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐬𝐨𝐦𝐞 𝐢𝐧𝐩𝐮𝐭 𝐲𝐞𝐬 𝐨𝐫 𝐧𝐨.\𝐧\𝐧𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐢𝐬 : **𝐨𝐧**"
                    )
                    return
            await event.reply(
                "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐬𝐨𝐦𝐞 𝐢𝐧𝐩𝐮𝐭 𝐲𝐞𝐬 𝐨𝐫 𝐧𝐨.\𝐧\𝐧𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐢𝐬 : **𝐨𝐟𝐟**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply(
                            "𝐆𝐥𝐨𝐛𝐚𝐥 𝐦𝐨𝐝𝐞 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭."
                        )
                        return
                globalchat.insert_one({"id": event.chat_id})
                await event.reply("𝐆𝐥𝐨𝐛𝐚𝐥 𝐦𝐨𝐝𝐞 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐧 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
        if input == "off":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        globalchat.delete_one({"id": event.chat_id})
                        await event.reply("𝐆𝐥𝐨𝐛𝐚𝐥 𝐦𝐨𝐝𝐞 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐟𝐟 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
                        return
            await event.reply("𝐆𝐥𝐨𝐛𝐚𝐥 𝐦𝐨𝐝𝐞 𝐢𝐬𝐧'𝐭 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐧 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.")
        if not input == "on" and not input == "off":
            await event.reply("𝐈 𝐨𝐧𝐥𝐲 𝐮𝐧𝐝𝐞𝐫𝐬𝐭𝐚𝐧𝐝 𝐛𝐲 𝐨𝐧 𝐨𝐫 𝐨𝐟𝐟")
            return
    else:
        await event.reply("`𝐘𝐨𝐮 𝐒𝐡𝐨𝐮𝐥𝐝 𝐁𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐃𝐨 𝐓𝐡𝐢𝐬!`")
        return


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    # let = sender.username
    if await is_admin(event, event.message.sender_id):
        return
    chats = spammers.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                if better_profanity.profanity.contains_profanity(msg):
                    await event.delete()
                    if sender.username is None:
                        st = sender.first_name
                        hh = sender.id
                        final = f"[{st}](tg://user?id={hh}) **{msg}** is detected as a slang word and your message has been deleted"
                    else:
                        final = f"Sir **{msg}** is detected as a slang word and your message has been deleted"
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()
        if event.photo:
            if event.chat_id == c["id"]:
                await event.client.download_media(event.photo, "nudes.jpg")
                if nude.is_nude("./nudes.jpg"):
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"**NSFW DETECTED**\n\n{st}](tg://user?id={hh}) your message contain NSFW content.. So, Lucas deleted the message\n\n **Nsfw Sender - User / Bot :** {st}](tg://user?id={hh})  \n\n`⚔️Automatic Detections Powered By LucasAI` \n**#GROUP_GUARDIAN** "
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()
                    os.remove("nudes.jpg")


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    # sender.username
    if await is_admin(event, event.message.sender_id):
        return
    chats = globalchat.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                u = msg.split()
                emj = extract_emojis(msg)
                msg = msg.replace(emj, "")
                if (
                    [(k) for k in u if k.startswith("@")]
                    and [(k) for k in u if k.startswith("#")]
                    and [(k) for k in u if k.startswith("/")]
                    and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
                ):
                    h = " ".join(filter(lambda x: x[0] != "@", u))
                    km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
                    tm = km.split()
                    jm = " ".join(filter(lambda x: x[0] != "#", tm))
                    hm = jm.split()
                    rm = " ".join(filter(lambda x: x[0] != "/", hm))
                elif [(k) for k in u if k.startswith("@")]:
                    rm = " ".join(filter(lambda x: x[0] != "@", u))
                elif [(k) for k in u if k.startswith("#")]:
                    rm = " ".join(filter(lambda x: x[0] != "#", u))
                elif [(k) for k in u if k.startswith("/")]:
                    rm = " ".join(filter(lambda x: x[0] != "/", u))
                elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
                    rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
                else:
                    rm = msg
                # print (rm)
                b = translator.detect(rm)
                if not "en" in b and not b == "":
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"[{st}](tg://user?id={hh}) you should only speak in english here !"
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()
#

__help__ = """
<b>✪ 𝐆𝐫𝐨𝐮𝐩 𝐆𝐮𝐚𝐫𝐝𝐢𝐚𝐧 ✪:</b>
✪ 𝐋𝐮𝐜𝐚𝐬 𝐜𝐚𝐧 𝐩𝐫𝐨𝐭𝐞𝐜𝐭 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐟𝐫𝐨𝐦 𝐍𝐒𝐅𝐖 𝐬𝐞𝐧𝐝𝐞𝐫𝐬, 𝐒𝐥𝐚𝐠 𝐰𝐨𝐫𝐝 𝐮𝐬𝐞𝐫𝐬 𝐚𝐧𝐝 𝐚𝐥𝐬𝐨 𝐜𝐚𝐧 𝐟𝐨𝐫𝐜𝐞 𝐦𝐞𝐦𝐛𝐞𝐫𝐬 𝐭𝐨 𝐮𝐬𝐞 𝐄𝐧𝐠𝐥𝐢𝐬𝐡

<b>𝐂𝐨𝐦𝐦𝐦𝐚𝐧𝐝𝐬</b>
⚫ - /gshield <𝐢>𝐨𝐧/𝐨𝐟𝐟</𝐢> - 𝐄𝐧𝐚𝐛𝐥𝐞|𝐃𝐢𝐬𝐚𝐛𝐥𝐞 𝐏𝐨𝐫𝐧 𝐜𝐥𝐞𝐚𝐧𝐢𝐧𝐠
⚫ - /globalmode <𝐢>𝐨𝐧/𝐨𝐟𝐟</𝐢> - 𝐄𝐧𝐚𝐛𝐥𝐞|𝐃𝐢𝐬𝐚𝐛𝐥𝐞 𝐄𝐧𝐠𝐥𝐢𝐬𝐡 𝐨𝐧𝐥𝐲 𝐦𝐨𝐝𝐞
⚫ - /profanity <𝐢>𝐨𝐧/𝐨𝐟𝐟</𝐢> - 𝐄𝐧𝐚𝐛𝐥𝐞|𝐃𝐢𝐬𝐚𝐛𝐥𝐞 𝐬𝐥𝐚𝐠 𝐰𝐨𝐫𝐝 𝐜𝐥𝐞𝐚𝐧𝐢𝐧𝐠
 
𝐍𝐨𝐭𝐞: 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐠𝐨𝐞𝐬 𝐭𝐨 @BotMasterOfficial
"""
__mod_name__ = "🛡️𝐒𝐡𝐢𝐞𝐥𝐝🛡️"
