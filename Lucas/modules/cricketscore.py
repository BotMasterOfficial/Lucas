# credits  @mkspali
# ported to Lucas @mkspali

import urllib.request

from bs4 import BeautifulSoup
from telethon import events
from Lucas import telethn as tbot
from telethon.tl import functions, types
from telethon.tl.types import *


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@tbot.on(events.NewMessage(pattern="/cs$"))
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       await event.reply("🚨 𝐍𝐞𝐞𝐝 𝐀𝐝𝐦𝐢𝐧 𝐏𝐞𝐰𝐞𝐫.. 𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.. 𝐁𝐮𝐭 𝐲𝐨𝐮 𝐜𝐚𝐧 𝐮𝐬𝐞 𝐢𝐧 𝐦𝐲 𝐩𝐦 🚨")
       return

    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = ""
    for match in result:
        Sed += match.get_text() + "\n\n"
    await event.reply(
        f"<b><u>𝐌𝐚𝐭𝐜𝐡 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐠𝐚𝐭𝐡𝐞𝐫𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲</b></u>\n\n\n<code>{Sed}</code>",
        parse_mode="HTML",
    )


__help__ = """
*𝐋𝐢𝐯𝐞 𝐜𝐫𝐢𝐜𝐤𝐞𝐭 𝐬𝐜𝐨𝐫𝐞*
⚫ /cs : 𝐋𝐚𝐭𝐞𝐬𝐭 𝐥𝐢𝐯𝐞 𝐬𝐜𝐨𝐫𝐞𝐬 𝐟𝐫𝐨𝐦 𝐜𝐫𝐢𝐜-𝐢𝐧𝐟𝐨
"""
__mod_name__ = "🏏𝐂𝐫𝐢𝐜𝐤𝐞𝐭🏏"
