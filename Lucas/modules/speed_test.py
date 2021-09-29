import speedtest
from Lucas import DEV_USERS, dispatcher
from Lucas.modules.disable import DisableAbleCommandHandler
from Lucas.modules.helper_funcs.chat_status import dev_plus
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, run_async


def convert(speed):
    return round(int(speed) / 1048576, 2)


@dev_plus
@run_async
def speedtestxyz(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("𝐈𝐦𝐚𝐠𝐞", callback_data="speedtest_image"),
            InlineKeyboardButton("𝐓𝐞𝐱𝐭", callback_data="speedtest_text"),
        ]
    ]
    update.effective_message.reply_text(
        "𝐒𝐞𝐥𝐞𝐜𝐭 𝐒𝐩𝐞𝐞𝐝𝐓𝐞𝐬𝐭 𝐌𝐨𝐝𝐞", reply_markup=InlineKeyboardMarkup(buttons)
    )


@run_async
def speedtestxyz_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text("𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐚 𝐒𝐩𝐞𝐞𝐝 𝐭𝐞𝐬𝐭....")
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = "𝐒𝐩𝐞𝐞𝐝 𝐓𝐞𝐬𝐭 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:"

        if query.data == "speedtest_image":
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(
                photo=speedtest_image, caption=replymsg
            )
            msg.delete()

        elif query.data == "speedtest_text":
            result = speed.results.dict()
            replymsg += f"\n𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝: `{convert(result['download'])}Mb/s`\n𝐔𝐩𝐥𝐨𝐚𝐝: `{convert(result['upload'])}Mb/s`\n𝐏𝐢𝐧𝐠: `{result['ping']}`"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("𝐘𝐨𝐮 𝐚𝐫𝐞 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐭𝐨 𝐣𝐨𝐢𝐧 @𝐁𝐨𝐭𝐌𝐚𝐬𝐭𝐞𝐫𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.")


SPEED_TEST_HANDLER = DisableAbleCommandHandler("speedtest", speedtestxyz)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(
    speedtestxyz_callback, pattern="speedtest_.*"
)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)

__mod_name__ = "SpeedTest"
__command_list__ = ["speedtest"]
__handlers__ = [SPEED_TEST_HANDLER, SPEED_TEST_CALLBACKHANDLER]
