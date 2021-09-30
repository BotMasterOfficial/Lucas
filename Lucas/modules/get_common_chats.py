import os
from time import sleep

from Lucas import OWNER_ID, dispatcher
from Lucas.modules.helper_funcs.extraction import extract_user
from Lucas.modules.sql.users_sql import get_user_com_chats
from telegram import Update
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async


@run_async
def get_user_common_chats(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    msg = update.effective_message
    user = extract_user(msg, args)
    if not user:
        msg.reply_text("𝐈 𝐬𝐡𝐚𝐫𝐞 𝐧𝐨 𝐜𝐨𝐦𝐦𝐨𝐧 𝐜𝐡𝐚𝐭𝐬 𝐰𝐢𝐭𝐡 𝐭𝐡𝐞 𝐯𝐨𝐢𝐝.")
        return
    common_list = get_user_com_chats(user)
    if not common_list:
        msg.reply_text("𝐍𝐨 𝐜𝐨𝐦𝐦𝐨𝐧 𝐜𝐡𝐚𝐭𝐬 𝐰𝐢𝐭𝐡 𝐭𝐡𝐢𝐬 𝐮𝐬𝐞𝐫!")
        return
    name = bot.get_chat(user).first_name
    text = f"<b>𝐂𝐨𝐦𝐦𝐨𝐧 𝐜𝐡𝐚𝐭𝐬 𝐰𝐢𝐭𝐡 {name}</b>\n"
    for chat in common_list:
        try:
            chat_name = bot.get_chat(chat).title
            sleep(0.3)
            text += f"• <code>{chat_name}</code>\n"
        except BadRequest:
            pass
        except Unauthorized:
            pass
        except RetryAfter as e:
            sleep(e.retry_after)

    if len(text) < 4096:
        msg.reply_text(text, parse_mode="HTML")
    else:
        with open("common_chats.txt", "w") as f:
            f.write(text)
        with open("common_chats.txt", "rb") as f:
            msg.reply_document(f)
        os.remove("common_chats.txt")


COMMON_CHATS_HANDLER = CommandHandler(
    "getchats", get_user_common_chats, filters=Filters.user(OWNER_ID)
)

dispatcher.add_handler(COMMON_CHATS_HANDLER)
