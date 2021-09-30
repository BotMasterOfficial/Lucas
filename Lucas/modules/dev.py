import os
import subprocess
import sys

from contextlib import suppress
from time import sleep

import Lucas

from Lucas import dispatcher
from Lucas.modules.helper_funcs.chat_status import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler, run_async

@run_async
@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.effective_message.reply_text(f"𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: {Lucas.ALLOW_CHATS}")
        return
    if args[0].lower() in ["off", "no"]:
        YoneRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        YoneRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("𝐅𝐨𝐫𝐦𝐚𝐭: /lockdown 𝐘𝐞𝐬/𝐍𝐨 𝐨𝐫 𝐎𝐟𝐟/𝐎𝐧")
        return
    update.effective_message.reply_text("𝐃𝐨𝐧𝐞! 𝐋𝐨𝐜𝐤𝐝𝐨𝐰𝐧 𝐯𝐚𝐥𝐮𝐞 𝐭𝐨𝐠𝐠𝐥𝐞𝐝.")

@run_async
@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "𝐁𝐞𝐞𝐩 𝐛𝐨𝐨𝐩, 𝐈 𝐜𝐨𝐮𝐥𝐝 𝐧𝐨𝐭 𝐥𝐞𝐚𝐯𝐞 𝐭𝐡𝐚𝐭 𝐠𝐫𝐨𝐮𝐩 ( 𝐃𝐨𝐧'𝐭 𝐤𝐧𝐨𝐰 𝐰𝐡𝐲 )."
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("𝐁𝐞𝐞𝐩 𝐛𝐨𝐨𝐩, 𝐈 𝐥𝐞𝐟𝐭 𝐭𝐡𝐚𝐭 𝐬𝐨𝐮𝐩!.")
    else:
        update.effective_message.reply_text("𝐒𝐞𝐧𝐝 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐜𝐡𝐚𝐭 𝐈𝐃")


@run_async
@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "𝐏𝐮𝐥𝐥𝐢𝐧𝐠 𝐚𝐥𝐥 𝐜𝐡𝐚𝐧𝐠𝐞𝐬 𝐟𝐫𝐨𝐦 𝐫𝐞𝐦𝐨𝐭𝐞 𝐚𝐧𝐝 𝐭𝐡𝐞𝐧 𝐚𝐭𝐭𝐞𝐦𝐩𝐭𝐢𝐧𝐠 𝐭𝐨 𝐫𝐞𝐬𝐭𝐚𝐫𝐭."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\n𝐂𝐡𝐚𝐧𝐠𝐞𝐬 𝐩𝐮𝐥𝐥𝐞𝐝...𝐈 𝐠𝐮𝐞𝐬𝐬.. 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐢𝐧 "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("✅ 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@run_async
@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐚 𝐧𝐞𝐰 𝐢𝐧𝐬𝐭𝐚𝐧𝐜𝐞 𝐚𝐧𝐝 𝐬𝐡𝐮𝐭𝐭𝐢𝐧𝐠 𝐝𝐨𝐰𝐧 𝐭𝐡𝐢𝐬 𝐨𝐧𝐞"
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("reboot", restart)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "Devs"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]
