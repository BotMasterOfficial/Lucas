import html
import random
import time

import Lucas.modules.fun_strings as fun_strings
from Lucas import dispatcher
from Lucas.modules.disable import DisableAbleCommandHandler
from Lucas.modules.helper_funcs.chat_status import is_user_admin
from Lucas.modules.helper_funcs.extraction import extract_user
from telegram import ChatPermissions, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, run_async

GIF_ID = "CgACAgQAAx0CSVUvGgAC7KpfWxMrgGyQs-GUUJgt-TSO8cOIDgACaAgAAlZD0VHT3Zynpr5nGxsE"


@run_async
def runs(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))


@run_async
def sanitize(update: Update, context: CallbackContext):
    message = update.effective_message
    name = (
        message.reply_to_message.from_user.first_name
        if message.reply_to_message
        else message.from_user.first_name
    )
    reply_animation = (
        message.reply_to_message.reply_animation
        if message.reply_to_message
        else message.reply_animation
    )
    reply_animation(GIF_ID, caption=f"*Sanitizes {name}*")


@run_async
def sanitize(update: Update, context: CallbackContext):
    message = update.effective_message
    name = (
        message.reply_to_message.from_user.first_name
        if message.reply_to_message
        else message.from_user.first_name
    )
    reply_animation = (
        message.reply_to_message.reply_animation
        if message.reply_to_message
        else message.reply_animation
    )
    reply_animation(random.choice(fun_strings.GIFS), caption=f"*Sanitizes {name}*")


@run_async
def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_LUCAS_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False),
                )
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    if update.effective_user.id == 1096215023:
        temp = "@NeoTheKitty scratches {user2}"

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun_strings.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun_strings.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun_strings.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))


@run_async
def shout(update: Update, context: CallbackContext):
    args = context.args
    text = " ".join(args)
    result = []
    result.append(" ".join(list(text)))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


@run_async
def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(fun_strings.TOSS))


@run_async
def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(r"¯\_(ツ)_/¯")


@run_async
def bluetext(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(
        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"
    )


@run_async
def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)


@run_async
def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.DECIDE))


@run_async
def eightball(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.EIGHTBALL))


@run_async
def table(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.TABLE))


normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


@run_async
def weebify(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    string = ""

    if message.reply_to_message:
        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:
        string = "  ".join(args).lower()

    if not string:
        message.reply_text("𝐔𝐬𝐚𝐠𝐞 𝐢𝐬 `/weebify <𝐭𝐞𝐱𝐭>`", parse_mode=ParseMode.MARKDOWN)
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)


__help__ = """
⚫ /runs*:* 𝐫𝐞𝐩𝐥𝐲 𝐚 𝐫𝐚𝐧𝐝𝐨𝐦 𝐬𝐭𝐫𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐚𝐧 𝐚𝐫𝐫𝐚𝐲 𝐨𝐟 𝐫𝐞𝐩𝐥𝐢𝐞𝐬
⚫ /slap*:* 𝐬𝐥𝐚𝐩 𝐚 𝐮𝐬𝐞𝐫, 𝐨𝐫 𝐠𝐞𝐭 𝐬𝐥𝐚𝐩𝐩𝐞𝐝 𝐢𝐟 𝐧𝐨𝐭 𝐚 𝐫𝐞𝐩𝐥𝐲
⚫ /shrug*:* 𝐠𝐞𝐭 𝐬𝐡𝐫𝐮𝐠 𝐗𝐃
⚫ /table*:* 𝐠𝐞𝐭 𝐟𝐥𝐢𝐩/𝐮𝐧𝐟𝐥𝐢𝐩 :𝐯
⚫ /decide*:* 𝐑𝐚𝐧𝐝𝐨𝐦𝐥𝐲 𝐚𝐧𝐬𝐰𝐞𝐫𝐬 𝐲𝐞𝐬/𝐧𝐨/𝐦𝐚𝐲𝐛𝐞
⚫ /toss*:* 𝐓𝐨𝐬𝐬𝐞𝐬 𝐀 𝐜𝐨𝐢𝐧
⚫ /bluetext*:* 𝐜𝐡𝐞𝐜𝐤 𝐮𝐫𝐬𝐞𝐥𝐟 :𝐕
⚫ /roll*:* 𝐑𝐨𝐥𝐥 𝐚 𝐝𝐢𝐜𝐞
⚫ /rlg*:* 𝐉𝐨𝐢𝐧 𝐞𝐚𝐫𝐬,𝐧𝐨𝐬𝐞,𝐦𝐨𝐮𝐭𝐡 𝐚𝐧𝐝 𝐜𝐫𝐞𝐚𝐭𝐞 𝐚𝐧 𝐞𝐦𝐨 ;-;
⚫ /shout <𝐤𝐞𝐲𝐰𝐨𝐫𝐝>*:* 𝐰𝐫𝐢𝐭𝐞 𝐚𝐧𝐲𝐭𝐡𝐢𝐧𝐠 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐠𝐢𝐯𝐞 𝐥𝐨𝐮𝐝 𝐬𝐡𝐨𝐮𝐭
⚫ /weebify <𝐭𝐞𝐱𝐭>*:* 𝐫𝐞𝐭𝐮𝐫𝐧𝐬 𝐚 𝐰𝐞𝐞𝐛𝐢𝐟𝐢𝐞𝐝 𝐭𝐞𝐱𝐭
⚫ /sanitize*:* 𝐚𝐥𝐰𝐚𝐲𝐬 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐞𝐟𝐨𝐫𝐞 /𝐩𝐚𝐭 𝐨𝐫 𝐚𝐧𝐲 𝐜𝐨𝐧𝐭𝐚𝐜𝐭
⚫ /pat*:* 𝐩𝐚𝐭𝐬 𝐚 𝐮𝐬𝐞𝐫, 𝐨𝐫 𝐠𝐞𝐭 𝐩𝐚𝐭𝐭𝐞𝐝
⚫ /8ball*:* 𝐩𝐫𝐞𝐝𝐢𝐜𝐭𝐬 𝐮𝐬𝐢𝐧𝐠 𝟖𝐛𝐚𝐥𝐥 𝐦𝐞𝐭𝐡𝐨𝐝
"""

SANITIZE_HANDLER = DisableAbleCommandHandler("sanitize", sanitize)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
ROLL_HANDLER = DisableAbleCommandHandler("roll", roll)
TOSS_HANDLER = DisableAbleCommandHandler("toss", toss)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext)
RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)
EIGHTBALL_HANDLER = DisableAbleCommandHandler("8ball", eightball)
TABLE_HANDLER = DisableAbleCommandHandler("table", table)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify)

dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(SANITIZE_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(BLUETEXT_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(EIGHTBALL_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)

__mod_name__ = "📝𝐌𝐞𝐦𝐞𝐬📝"
__command_list__ = [
    "runs",
    "slap",
    "roll",
    "toss",
    "shrug",
    "bluetext",
    "rlg",
    "decide",
    "table",
    "pat",
    "sanitize",
    "shout",
    "weebify",
    "8ball",
]
__handlers__ = [
    RUNS_HANDLER,
    SLAP_HANDLER,
    PAT_HANDLER,
    ROLL_HANDLER,
    TOSS_HANDLER,
    SHRUG_HANDLER,
    BLUETEXT_HANDLER,
    RLG_HANDLER,
    DECIDE_HANDLER,
    TABLE_HANDLER,
    SANITIZE_HANDLER,
    SHOUT_HANDLER,
    WEEBIFY_HANDLER,
    EIGHTBALL_HANDLER,
]
