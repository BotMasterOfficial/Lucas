from typing import List, Optional

from Lucas import LOGGER
from Lucas.modules.users import get_user_id
from telegram import Message, MessageEntity
from telegram.error import BadRequest


def id_from_reply(message):
    prev_message = message.reply_to_message
    if not prev_message:
        return None, None
    user_id = prev_message.from_user.id
    res = message.text.split(None, 1)
    if len(res) < 2:
        return user_id, ""
    return user_id, res[1]


def extract_user(message: Message, args: List[str]) -> Optional[int]:
    return extract_user_and_text(message, args)[0]


def extract_user_and_text(
    message: Message, args: List[str]
) -> (Optional[int], Optional[str]):
    prev_message = message.reply_to_message
    split_text = message.text.split(None, 1)

    if len(split_text) < 2:
        return id_from_reply(message)  # only option possible

    text_to_parse = split_text[1]

    text = ""

    entities = list(message.parse_entities([MessageEntity.TEXT_MENTION]))
    ent = entities[0] if entities else None
    # if entity offset matches (command end/text start) then all good
    if entities and ent and ent.offset == len(message.text) - len(text_to_parse):
        ent = entities[0]
        user_id = ent.user.id
        text = message.text[ent.offset + ent.length :]

    elif len(args) >= 1 and args[0][0] == "@":
        user = args[0]
        user_id = get_user_id(user)
        if not user_id:
            message.reply_text(
                "𝐍𝐨 𝐢𝐝𝐞𝐚 𝐰𝐡𝐨 𝐭𝐡𝐢𝐬 𝐮𝐬𝐞𝐫 𝐢𝐬. 𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐚𝐛𝐥𝐞 𝐭𝐨 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭 𝐰𝐢𝐭𝐡 𝐭𝐡𝐞𝐦 𝐢𝐟 "
                "𝐘𝐨𝐮 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐭𝐡𝐚𝐭 𝐩𝐞𝐫𝐬𝐨𝐧'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐢𝐧𝐬𝐭𝐞𝐚𝐝, 𝐨𝐫 𝐟𝐨𝐫𝐰𝐚𝐫𝐝 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐚𝐭 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬."
            )
            return None, None

        else:
            user_id = user_id
            res = message.text.split(None, 2)
            if len(res) >= 3:
                text = res[2]

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])
        res = message.text.split(None, 2)
        if len(res) >= 3:
            text = res[2]

    elif prev_message:
        user_id, text = id_from_reply(message)

    else:
        return None, None

    try:
        message.bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in ("User_id_invalid", "Chat not found"):
            message.reply_text(
                "𝐈 𝐝𝐨𝐧'𝐭 𝐬𝐞𝐞𝐦 𝐭𝐨 𝐡𝐚𝐯𝐞 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭𝐞𝐝 𝐰𝐢𝐭𝐡 𝐭𝐡𝐢𝐬 𝐮𝐬𝐞𝐫 𝐛𝐞𝐟𝐨𝐫𝐞 - 𝐩𝐥𝐞𝐚𝐬𝐞 𝐟𝐨𝐫𝐰𝐚𝐫𝐝 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐫𝐨𝐦 "
                "𝐭𝐡𝐞𝐦 𝐭𝐨 𝐠𝐢𝐯𝐞 𝐦𝐞 𝐜𝐨𝐧𝐭𝐫𝐨𝐥! (𝐥𝐢𝐤𝐞 𝐚 𝐯𝐨𝐨𝐝𝐨𝐨 𝐝𝐨𝐥𝐥, 𝐈 𝐧𝐞𝐞𝐝 𝐚 𝐩𝐢𝐞𝐜𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐭𝐨 𝐛𝐞 𝐚𝐛𝐥𝐞 "
                "𝐭𝐨 𝐞𝐱𝐞𝐜𝐮𝐭𝐞 𝐜𝐞𝐫𝐭𝐚𝐢𝐧 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬...)"
            )
        else:
            LOGGER.exception("Exception %s on user %s", excp.message, user_id)

        return None, None

    return user_id, text


def extract_text(message) -> str:
    return (
        message.text
        or message.caption
        or (message.sticker.emoji if message.sticker else None)
    )


def extract_unt_fedban(
    message: Message, args: List[str]
) -> (Optional[int], Optional[str]):
    prev_message = message.reply_to_message
    split_text = message.text.split(None, 1)

    if len(split_text) < 2:
        return id_from_reply(message)  # only option possible

    text_to_parse = split_text[1]

    text = ""

    entities = list(message.parse_entities([MessageEntity.TEXT_MENTION]))
    ent = entities[0] if entities else None
    # if entity offset matches (command end/text start) then all good
    if entities and ent and ent.offset == len(message.text) - len(text_to_parse):
        ent = entities[0]
        user_id = ent.user.id
        text = message.text[ent.offset + ent.length :]

    elif len(args) >= 1 and args[0][0] == "@":
        user = args[0]
        user_id = get_user_id(user)
        if not user_id and not isinstance(user_id, int):
            message.reply_text(
                "𝐈 𝐝𝐨𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐭𝐡𝐚𝐭 𝐮𝐬𝐞𝐫 𝐢𝐧 𝐦𝐲 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞.  "
                "𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐚𝐛𝐥𝐞 𝐭𝐨 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭 𝐰𝐢𝐭𝐡 𝐭𝐡𝐞𝐦 𝐢𝐟 𝐲𝐨𝐮 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐭𝐡𝐚𝐭 𝐩𝐞𝐫𝐬𝐨𝐧'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐢𝐧𝐬𝐭𝐞𝐚𝐝, 𝐨𝐫 𝐟𝐨𝐫𝐰𝐚𝐫𝐝 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐚𝐭 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬."
            )
            return None, None

        else:
            user_id = user_id
            res = message.text.split(None, 2)
            if len(res) >= 3:
                text = res[2]

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])
        res = message.text.split(None, 2)
        if len(res) >= 3:
            text = res[2]

    elif prev_message:
        user_id, text = id_from_reply(message)

    else:
        return None, None

    try:
        message.bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in ("User_id_invalid", "Chat not found") and not isinstance(
            user_id, int
        ):
            message.reply_text(
                "𝐈 𝐝𝐨𝐧'𝐭 𝐬𝐞𝐞𝐦 𝐭𝐨 𝐡𝐚𝐯𝐞 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭𝐞𝐝 𝐰𝐢𝐭𝐡 𝐭𝐡𝐢𝐬 𝐮𝐬𝐞𝐫 𝐛𝐞𝐟𝐨𝐫𝐞 - 𝐩𝐥𝐞𝐚𝐬𝐞 𝐟𝐨𝐫𝐰𝐚𝐫𝐝 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐫𝐨𝐦 "
                "𝐭𝐡𝐞𝐦 𝐭𝐨 𝐠𝐢𝐯𝐞 𝐦𝐞 𝐜𝐨𝐧𝐭𝐫𝐨𝐥! (𝐥𝐢𝐤𝐞 𝐚 𝐯𝐨𝐨𝐝𝐨𝐨 𝐝𝐨𝐥𝐥, 𝐈 𝐧𝐞𝐞𝐝 𝐚 𝐩𝐢𝐞𝐜𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐭𝐨 𝐛𝐞 𝐚𝐛𝐥𝐞 "
                "𝐭𝐨 𝐞𝐱𝐞𝐜𝐮𝐭𝐞 𝐜𝐞𝐫𝐭𝐚𝐢𝐧 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬...)"
            )
            return None, None
        elif excp.message != "𝗖𝗵𝗮𝘁 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱":
            LOGGER.exception("Exception %s on user %s", excp.message, user_id)
            return None, None
        elif not isinstance(user_id, int):
            return None, None

    return user_id, text


def extract_user_fban(message: Message, args: List[str]) -> Optional[int]:
    return extract_unt_fedban(message, args)[0]
