import importlib
import time
import re
from sys import argv
from typing import Optional

from Lucas import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Lucas.modules import ALL_MODULES
from Lucas.modules.helper_funcs.chat_status import is_user_admin
from Lucas.modules.helper_funcs.misc import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
𝐇𝐞𝐥𝐥𝐨 {},

⚫ 𝐈 𝐚𝐦 𝐋𝐮𝐜𝐚𝐬, 𝐇𝐢𝐠𝐡𝐥𝐲 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐁𝐨𝐭 𝐰𝐢𝐭𝐡 𝐥𝐨𝐭𝐬 𝐨𝐟 𝐚𝐦𝐚𝐳𝐢𝐧𝐠 𝐭𝐨𝐨𝐥𝐬

⚫ 𝐈 𝐚𝐦 𝐡𝐞𝐫𝐞 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐌𝐚𝐧𝐚𝐠𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐠𝐫𝐨𝐮𝐩𝐬

⚫ 𝐇𝐢𝐭 /help   
"""

buttons = [
    [
        InlineKeyboardButton(
            text="➕️ 𝐀𝐃𝐃 𝐋𝐔𝐂𝐀𝐒 𝐓𝐎 𝐆𝐑𝐎𝐔𝐏 ➕️", url="t.me/LucasOfficialBot?startgroup=true"),
    ],
    [
        InlineKeyboardButton(text="💠𝐀𝐁𝐎𝐔𝐓💠", callback_data="lucas_"),
        InlineKeyboardButton(
            text="🫂𝐒𝐔𝐏𝐏𝐎𝐑𝐓🫂", url=f"https://t.me/{SUPPORT_CHAT}"
        ),
    ],
    [
        InlineKeyboardButton(text="🆘𝐇𝐄𝐋𝐏 & 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒🆘", callback_data="help_back"),
    ],
]


HELP_STRINGS = """
`𝐇𝐞𝐥𝐥𝐨 {},𝐈 𝐚𝐦 𝐋𝐮𝐜𝐚𝐬 [🙋‍♀️](https://telegra.ph/file/8db76d7aa4f2aee630167.jpg) 
`𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐓𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧𝐬 𝐁𝐞𝐥𝐨𝐰 𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐜𝐮𝐦𝐞𝐧𝐭𝐚𝐭𝐢𝐨𝐧 𝐀𝐛𝐨𝐮𝐭 𝐒𝐩𝐞𝐜𝐢𝐟𝐢𝐜 𝐌𝐨𝐝𝐮𝐥𝐞𝐬 ....`"""

lucas_IMG = "https://telegra.ph/file/8db76d7aa4f2aee630167.jpg"

DONATE_STRING = """𝐇𝐞𝐲𝐚, 𝐠𝐥𝐚𝐝 𝐭𝐨 𝐡𝐞𝐚𝐫 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐝𝐨𝐧𝐚𝐭𝐞!
 𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐭𝐡𝐞 𝐩𝐫𝐨𝐣𝐞𝐜𝐭 𝐛𝐲 𝐜𝐨𝐧𝐭𝐚𝐜𝐭𝐢𝐧𝐠 @mkspali \
 𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐢𝐧𝐠 𝐢𝐬 𝐧𝐨𝐭 𝐚𝐥𝐰𝐚𝐲𝐬 𝐟𝐢𝐧𝐚𝐧𝐜𝐢𝐚𝐥! \
 𝐓𝐡𝐨𝐬𝐞 𝐰𝐡𝐨 𝐜𝐚𝐧𝐧𝐨𝐭 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐦𝐨𝐧𝐞𝐭𝐚𝐫𝐲 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐚𝐫𝐞 𝐰𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐮𝐬 𝐝𝐞𝐯𝐞𝐥𝐨𝐩 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐚𝐭 ."""

TECHNO_IMG = "https://telegra.ph/file/8db76d7aa4f2aee630167.jpg"
IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Lucas.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK ➡️", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_text(
            "I am awake already!\n<b>Haven't slept since:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


@run_async
def yone_about_callback(update, context):
    query = update.callback_query
    if query.data == "Lucas_":
        query.message.edit_text(
            text=""" ℹ️ 𝐈 𝐚𝐦 *𝐋𝐮𝐜𝐚𝐬*, 𝐚 𝐩𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐠𝐫𝐨𝐮𝐩 𝐦𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 𝐛𝐨𝐭 𝐛𝐮𝐢𝐥𝐭 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐦𝐚𝐧𝐚𝐠𝐞 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐞𝐚𝐬𝐢𝐥𝐲.
                 \n⚫ 𝐈 𝐜𝐚𝐧 𝐫𝐞𝐬𝐭𝐫𝐢𝐜𝐭 𝐮𝐬𝐞𝐫𝐬.
                 \n⚫ 𝐈 𝐜𝐚𝐧 𝐠𝐫𝐞𝐞𝐭 𝐮𝐬𝐞𝐫𝐬 𝐰𝐢𝐭𝐡 𝐜𝐮𝐬𝐭𝐨𝐦𝐢𝐳𝐚𝐛𝐥𝐞 𝐰𝐞𝐥𝐜𝐨𝐦𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐚𝐧𝐝 𝐞𝐯𝐞𝐧 𝐬𝐞𝐭 𝐚 𝐠𝐫𝐨𝐮𝐩'𝐬 𝐫𝐮𝐥𝐞𝐬.
                 \n⚫ 𝐈 𝐡𝐚𝐯𝐞 𝐚𝐧 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐚𝐧𝐭𝐢-𝐟𝐥𝐨𝐨𝐝 𝐬𝐲𝐬𝐭𝐞𝐦.
                 \n⚫ 𝐈 𝐜𝐚𝐧 𝐰𝐚𝐫𝐧 𝐮𝐬𝐞𝐫𝐬 𝐮𝐧𝐭𝐢𝐥 𝐭𝐡𝐞𝐲 𝐫𝐞𝐚𝐜𝐡 𝐦𝐚𝐱 𝐰𝐚𝐫𝐧𝐬, 𝐰𝐢𝐭𝐡 𝐞𝐚𝐜𝐡 𝐩𝐫𝐞𝐝𝐞𝐟𝐢𝐧𝐞𝐝 𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐬𝐮𝐜𝐡 𝐚𝐬 𝐛𝐚𝐧, 𝐦𝐮𝐭𝐞, 𝐤𝐢𝐜𝐤, 𝐞𝐭𝐜.
                 \n⚫ 𝐈 𝐡𝐚𝐯𝐞 𝐚 𝐧𝐨𝐭𝐞 𝐤𝐞𝐞𝐩𝐢𝐧𝐠 𝐬𝐲𝐬𝐭𝐞𝐦, 𝐛𝐥𝐚𝐜𝐤𝐥𝐢𝐬𝐭𝐬, 𝐚𝐧𝐝 𝐞𝐯𝐞𝐧 𝐩𝐫𝐞𝐝𝐞𝐭𝐞𝐫𝐦𝐢𝐧𝐞𝐝 𝐫𝐞𝐩𝐥𝐢𝐞𝐬 𝐨𝐧 𝐜𝐞𝐫𝐭𝐚𝐢𝐧 𝐤𝐞𝐲𝐰𝐨𝐫𝐝𝐬.
                 \n⚫ 𝐈 𝐜𝐡𝐞𝐜𝐤 𝐟𝐨𝐫 𝐚𝐝𝐦𝐢𝐧𝐬' 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐛𝐞𝐟𝐨𝐫𝐞 𝐞𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠 𝐚𝐧𝐲 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐚𝐧𝐝 𝐦𝐨𝐫𝐞 𝐬𝐭𝐮𝐟𝐟𝐬
                 \n⚫ 𝐋𝐮𝐜𝐚𝐬'𝐬 𝐥𝐢𝐜𝐞𝐧𝐬𝐞𝐝 𝐮𝐧𝐝𝐞𝐫 𝐭𝐡𝐞 𝐆𝐍𝐔 𝐆𝐞𝐧𝐞𝐫𝐚𝐥 𝐏𝐮𝐛𝐥𝐢𝐜 𝐋𝐢𝐜𝐞𝐧𝐬𝐞 𝐯𝟑.𝟎
                 \n⚫ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐭𝐡𝐞 [💾𝐑𝐞𝐩𝐨𝐬𝐢𝐭𝐨𝐫𝐲💾](https://github.com/BotMasterOfficial/Lucas)
                 \n⚫ 𝐈𝐟 𝐲𝐨𝐮 𝐡𝐚𝐯𝐞 𝐚𝐧𝐲 𝐪𝐮𝐞𝐬𝐭𝐢𝐨𝐧 𝐚𝐛𝐨𝐮𝐭 𝐲𝐨𝐧𝐞, 𝐥𝐞𝐭 𝐮𝐬 𝐤𝐧𝐨𝐰 𝐚𝐭 @BotMasterOfficial""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="lucas_back")
                 ]
                ]
            ),
        )
    elif query.data == "lucas_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )


@run_async
def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=""" 𝐇𝐞𝐥𝐥𝐨..🤗 𝐈 𝐚𝐦 *𝐋𝐮𝐜𝐚𝐬*
                 \n𝐇𝐞𝐫𝐞 𝐢𝐬 𝐭𝐡𝐞 [𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞](https://github.com/BotMasterOfficial/Lucas) .""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Go Back", callback_data="source_back")
                 ]
                ]
            ),
        )
    elif query.data == "source_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "𝐓𝐡𝐞𝐬𝐞 𝐚𝐫𝐞 𝐲𝐨𝐮𝐫 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "𝐒𝐞𝐞𝐦𝐬 𝐥𝐢𝐤𝐞 𝐭𝐡𝐞𝐫𝐞 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐧𝐲 𝐮𝐬𝐞𝐫 𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐜 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "𝐒𝐞𝐞𝐦𝐬 𝐥𝐢𝐤𝐞 𝐭𝐡𝐞𝐫𝐞 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐧𝐲 𝐮𝐬𝐞𝐫 𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐜 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 :'(\nSend this "
                "𝐢𝐧 𝐚 𝐠𝐫𝐨𝐮𝐩 𝐜𝐡𝐚𝐭 𝐲𝐨𝐮'𝐫𝐞 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐨 𝐟𝐢𝐧𝐝 𝐢𝐭𝐬 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "𝐇𝐢 𝐭𝐡𝐞𝐫𝐞! 𝐓𝐡𝐞𝐫𝐞 𝐚𝐫𝐞 𝐪𝐮𝐢𝐭𝐞 𝐚 𝐟𝐞𝐰 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐟𝐨𝐫 {} - 𝐠𝐨 𝐚𝐡𝐞𝐚𝐝 𝐚𝐧𝐝 𝐩𝐢𝐜𝐤 𝐰𝐡𝐚𝐭 "
                "𝐲𝐨𝐮'𝐫𝐞 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭𝐞𝐝 𝐢𝐧.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "𝐇𝐢 𝐭𝐡𝐞𝐫𝐞! 𝐓𝐡𝐞𝐫𝐞 𝐚𝐫𝐞 𝐪𝐮𝐢𝐭𝐞 𝐚 𝐟𝐞𝐰 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐟𝐨𝐫 {} - 𝐠𝐨 𝐚𝐡𝐞𝐚𝐝 𝐚𝐧𝐝 𝐩𝐢𝐜𝐤 𝐰𝐡𝐚𝐭 "
                "𝐲𝐨𝐮'𝐫𝐞 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭𝐞𝐝 𝐢𝐧.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="𝐇𝐢 𝐭𝐡𝐞𝐫𝐞! 𝐓𝐡𝐞𝐫𝐞 𝐚𝐫𝐞 𝐪𝐮𝐢𝐭𝐞 𝐚 𝐟𝐞𝐰 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐟𝐨𝐫 {} - 𝐠𝐨 𝐚𝐡𝐞𝐚𝐝 𝐚𝐧𝐝 𝐩𝐢𝐜𝐤 𝐰𝐡𝐚𝐭 "
                "𝐲𝐨𝐮'𝐫𝐞 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭𝐞𝐝 𝐢𝐧.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "𝐂𝐥𝐢𝐜𝐤 𝐡𝐞𝐫𝐞 𝐭𝐨 𝐠𝐞𝐭 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭'𝐬 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬, 𝐚𝐬 𝐰𝐞𝐥𝐥 𝐚𝐬 𝐲𝐨𝐮𝐫𝐬."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "𝐂𝐥𝐢𝐜𝐤 𝐡𝐞𝐫𝐞 𝐭𝐨 𝐜𝐡𝐞𝐜𝐤 𝐲𝐨𝐮𝐫 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 412094015 and DONATION_LINK:
            update.effective_message.reply_text(
                "𝐘𝐨𝐮 𝐜𝐚𝐧 𝐚𝐥𝐬𝐨 𝐝𝐨𝐧𝐚𝐭𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐩𝐞𝐫𝐬𝐨𝐧 𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐫𝐮𝐧𝐧𝐢𝐧𝐠 𝐦𝐞 "
                "[𝐇𝐞𝐫𝐞]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "𝐈'𝐯𝐞 𝐏𝐌'𝐞𝐝 𝐲𝐨𝐮 𝐚𝐛𝐨𝐮𝐭 𝐝𝐨𝐧𝐚𝐭𝐢𝐧𝐠 𝐭𝐨 𝐦𝐲 𝐜𝐫𝐞𝐚𝐭𝐨𝐫!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐦𝐞 𝐢𝐧 𝐏𝐌 𝐟𝐢𝐫𝐬𝐭 𝐭𝐨 𝐠𝐞𝐭 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "𝐘𝐞𝐬 𝐈'𝐦 𝐚𝐥𝐢𝐯𝐞 😹")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(lucas_about_callback, pattern=r"lucas_")
    source_callback_handler = CallbackQueryHandler(Source_about_callback, pattern=r"source_")

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
