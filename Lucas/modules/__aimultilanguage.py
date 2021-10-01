import re

import emoji

IBM_WATSON_CRED_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/bd6b59ba-3134-4dd4-aff2-49a79641ea15"
IBM_WATSON_CRED_PASSWORD = "UQ1MtTzZhEsMGK094klnfa-7y_4MCpJY1yhd52MXOo3Y"
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
import re

import aiohttp
from google_trans_new import google_translator
from pyrogram import filters

from Lucas import BOT_ID
from Lucas.helper_extra.aichat import add_chat, get_session, remove_chat
from Lucas.pyrogramee.pluginshelper import admins_only, edit_or_reply
from Lucas import pbot as Lucas

translator = google_translator()
import requests


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


lucas_chats = []
en_chats = []

@Lucas.on_message(
    filters.command("chatbot") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def hmm(_, message):
    global lucas_chats
    if len(message.command) != 2:
        await message.reply_text(
            "𝐈 𝐨𝐧𝐥𝐲 𝐫𝐞𝐜𝐨𝐠𝐧𝐢𝐳𝐞 `/chatbot on` and /chatbot `off only`"
        )
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`Processing...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("𝐋𝐮𝐜𝐚𝐬 𝐀𝐈 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭")
            return
        await lel.edit(
            f"𝐋𝐮𝐜𝐚𝐬 𝐀𝐈 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐀𝐝𝐝𝐞𝐝 𝐅𝐨𝐫 𝐔𝐬𝐞𝐫𝐬 𝐈𝐧 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭 {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`Processing...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("𝐋𝐮𝐜𝐚𝐬 𝐀𝐈 𝐖𝐚𝐬 𝐍𝐨𝐭 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭")
            return
        await lel.edit(
            f"𝐋𝐮𝐜𝐚𝐬 𝐀𝐈 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐞𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐅𝐨𝐫 𝐔𝐬𝐞𝐫𝐬 𝐈𝐧 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭 {message.chat.id}"
        )

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text("𝐄𝐧𝐠𝐥𝐢𝐬𝐡 𝐀𝐈 𝐜𝐡𝐚𝐭 𝐄𝐧𝐚𝐛𝐥𝐞𝐝!")
            return
        await message.reply_text("𝐀𝐈 𝐂𝐡𝐚𝐭 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝.")
        message.continue_propagation()
    else:
        await message.reply_text(
            "I only recognize `/chatbot on` and /chatbot `off only`"
        )


@Lucas.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("lucas", "Aco")
        test = test.replace("lucas", "Aco")
        URL = "https://api.affiliateplus.xyz/api/chatbot?message=hi&botname=@LucasOfficialBot&ownername=@mkspali"

        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return

        pro = result["message"]
        try:
            await Lucas.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
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
        try:
            lan = translator.detect(rm)
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, lang_tgt="en")
            except:
                return
        # test = emoji.demojize(test.strip())

        # Kang with the credits bitches @mkspali
        test = test.replace("lucas", "Aco")
        test = test.replace("lucas", "Aco")
        URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@LucasOfficialBot&ownername=@mkspali"
        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return
        pro = result["message"]
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, lang_tgt=lan[0])
            except:
                return
        try:
            await Lucas.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@Lucas.on_message(
    filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
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
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @mkspali
    test = test.replace("lucas", "Aco")
    test = test.replace("lucas", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@LucasOfficialBot&ownername=@mkspali"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return

    pro = result["message"]
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, lang_tgt=lan[0])
    try:
        await Lucas.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@Lucas.on_message(
    filters.regex("lucas|lucas|Lucas|Lucas|Lucas")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
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
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @mkspali
    test = test.replace("lucas", "Aco")
    test = test.replace("lucas", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@LucasOfficialBot&ownername=@mkspali"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return
    pro = result["message"]
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, lang_tgt=lan[0])
        except Exception:
            return
    try:
        await Lucas.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
𝐂𝐡𝐚𝐭𝐁𝐨𝐭
𝐋𝐮𝐜𝐚𝐬 𝐀𝐈 𝟑.𝟎 𝐈𝐒 𝐓𝐡𝐞 𝐎𝐧𝐥𝐲 𝐀𝐈 𝐒𝐲𝐬𝐭𝐞𝐦 𝐖𝐡𝐢𝐜𝐡 𝐂𝐚𝐧 𝐃𝐞𝐭𝐞𝐜𝐭 & 𝐑𝐞𝐩𝐥𝐲 𝐔𝐩𝐭𝐨 𝟐𝟎𝟎 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞
 - /chatbot [ON/OFF]: 𝐄𝐧𝐚𝐛𝐥𝐞𝐬 𝐚𝐧𝐝 𝐝𝐢𝐬𝐚𝐛𝐥𝐞𝐬 𝐀𝐈 𝐂𝐡𝐚𝐭 𝐦𝐨𝐝𝐞 (𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄)
 - /chatbot EN : 𝐄𝐧𝐚𝐛𝐥𝐞𝐬 𝐄𝐧𝐠𝐥𝐢𝐬𝐡 𝐨𝐧𝐥𝐲 𝐜𝐡𝐚𝐭𝐛𝐨𝐭
 
"""

__mod_name__ = "🗨️𝐂𝐡𝐚𝐭𝐁𝐨𝐭🗨️"
