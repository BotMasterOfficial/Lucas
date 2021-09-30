from Lucas import telethn as tbot
import os
import urllib.request
from datetime import datetime
from typing import List
from typing import Optional
import requests
from telethon import *
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from Lucas import *
from Lucas.events import register


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


@register(pattern="^/stt$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       await event.reply("⚠️ 𝐍𝐞𝐞𝐝 𝐀𝐝𝐦𝐢𝐧 𝐏𝐨𝐰𝐞𝐫.. 𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.. 𝐁𝐮𝐭 𝐲𝐨𝐮 𝐜𝐚𝐧 𝐮𝐬𝐞 𝐢𝐧 𝐦𝐲 𝐩𝐦 ")
       return

    start = datetime.now()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await event.client.download_media(
            previous_message, TEMP_DOWNLOAD_DIRECTORY
        )
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.reply(
                "You need to set the required ENV variables for this module. \nModule stopping"
            )
        else:
            # await event.reply("Starting analysis")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"])
                    transcript_confidence += (
                        " " + str(alternatives["confidence"]) + " + "
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = "TRANSCRIPT: `{}`\nTime Taken: {} seconds\nConfidence: `{}`".format(
                        transcript_response, ms, transcript_confidence
                    )
                else:
                    string_to_show = "TRANSCRIPT: `Nil`\nTime Taken: {} seconds\n\n**No Results Found**".format(
                        ms
                    )
                await event.reply(string_to_show)
            else:
                await event.reply(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.reply("Reply to a voice message, to get the text out of it.")


__help__ = """
𝐈 𝐜𝐚𝐧 𝐜𝐨𝐧𝐯𝐞𝐫𝐭 𝐭𝐞𝐱𝐭 𝐭𝐨 𝐯𝐨𝐢𝐜𝐞 𝐚𝐧𝐝 𝐯𝐨𝐢𝐜𝐞 𝐭𝐨 𝐭𝐞𝐱𝐭..
⚫ /tts <𝐥𝐚𝐧𝐠 𝐜𝐨𝐝𝐞>*:* 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚𝐧𝐲 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐨 𝐠𝐞𝐭 𝐭𝐞𝐱𝐭 𝐭𝐨 𝐬𝐩𝐞𝐞𝐜𝐡 𝐨𝐮𝐭𝐩𝐮𝐭
⚫ /stt*:* 𝐓𝐲𝐩𝐞 𝐢𝐧 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐨𝐢𝐜𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞(𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐞𝐧𝐠𝐥𝐢𝐬𝐡 𝐨𝐧𝐥𝐲) 𝐭𝐨 𝐞𝐱𝐭𝐫𝐚𝐜𝐭 𝐭𝐞𝐱𝐭 𝐟𝐫𝐨𝐦 𝐢𝐭.
*𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞 𝐂𝐨𝐝𝐞𝐬*
`𝐚𝐟,𝐚𝐦,𝐚𝐫,𝐚𝐳,𝐛𝐞,𝐛𝐠,𝐛𝐧,𝐛𝐬,𝐜𝐚,𝐜𝐞𝐛,𝐜𝐨,𝐜𝐬,𝐜𝐲,𝐝𝐚,𝐝𝐞,𝐞𝐥,𝐞𝐧,𝐞𝐨,𝐞𝐬,
𝐞𝐭,𝐞𝐮,𝐟𝐚,𝐟𝐢,𝐟𝐫,𝐟𝐲,𝐠𝐚,𝐠𝐝,𝐠𝐥,𝐠𝐮,𝐡𝐚,𝐡𝐚𝐰,𝐡𝐢,𝐡𝐦𝐧,𝐡𝐫,𝐡𝐭,𝐡𝐮,𝐡𝐲,
𝐢𝐝,𝐢𝐠,𝐢𝐬,𝐢𝐭,𝐢𝐰,𝐣𝐚,𝐣𝐰,𝐤𝐚,𝐤𝐤,𝐤𝐦,𝐤𝐧,𝐤𝐨,𝐤𝐮,𝐤𝐲,𝐥𝐚,𝐥𝐛,𝐥𝐨,𝐥𝐭,𝐥𝐯,𝐦𝐠,𝐦𝐢,𝐦𝐤,
𝐦𝐥,𝐦𝐧,𝐦𝐫,𝐦𝐬,𝐦𝐭,𝐦𝐲,𝐧𝐞,𝐧𝐥,𝐧𝐨,𝐧𝐲,𝐩𝐚,𝐩𝐥,𝐩𝐬,𝐩𝐭,𝐫𝐨,𝐫𝐮,𝐬𝐝,𝐬𝐢,𝐬𝐤,𝐬𝐥,
𝐬𝐦,𝐬𝐧,𝐬𝐨,𝐬𝐪,𝐬𝐫,𝐬𝐭,𝐬𝐮,𝐬𝐯,𝐬𝐰,𝐭𝐚,𝐭𝐞,𝐭𝐠,𝐭𝐡,𝐭𝐥,𝐭𝐫,𝐮𝐤,𝐮𝐫,𝐮𝐳,
𝐯𝐢,𝐱𝐡,𝐲𝐢,𝐲𝐨,𝐳𝐡,𝐳𝐡_𝐂𝐍,𝐳𝐡_𝐓𝐖,𝐳𝐮`
"""

__mod_name__ = "📝𝐓𝐓𝐒/𝐒𝐓𝐓📝"
