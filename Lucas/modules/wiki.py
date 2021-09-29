import wikipedia
from Lucas import dispatcher
from Lucas.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async
from wikipedia.exceptions import DisambiguationError, PageError


@run_async
def wiki(update: Update, context: CallbackContext):
    msg = (
        update.effective_message.reply_to_message
        if update.effective_message.reply_to_message
        else update.effective_message
    )
    res = ""
    if msg == update.effective_message:
        search = msg.text.split(" ", maxsplit=1)[1]
    else:
        search = msg.text
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        update.message.reply_text(
            "𝐃𝐢𝐬𝐚𝐦𝐛𝐢𝐠𝐮𝐚𝐭𝐞𝐝 𝐩𝐚𝐠𝐞𝐬 𝐟𝐨𝐮𝐧𝐝! 𝐀𝐝𝐣𝐮𝐬𝐭 𝐲𝐨𝐮𝐫 𝐪𝐮𝐞𝐫𝐲 𝐚𝐜𝐜𝐨𝐫𝐝𝐢𝐧𝐠𝐥𝐲.\n<i>{}</i>".format(
                e
            ),
            parse_mode=ParseMode.HTML,
        )
    except PageError as e:
        update.message.reply_text(
            "<code>{}</code>".format(e), parse_mode=ParseMode.HTML
        )
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">𝐑𝐞𝐚𝐝 𝐦𝐨𝐫𝐞...</a>"""
        if len(result) > 4000:
            with open("result.txt", "w") as f:
                f.write(f"{result}\n\nUwU OwO OmO UmU")
            with open("result.txt", "rb") as f:
                context.bot.send_document(
                    document=f,
                    filename=f.name,
                    reply_to_message_id=update.message.message_id,
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
                )
        else:
            update.message.reply_text(
                result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )


WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki)
dispatcher.add_handler(WIKI_HANDLER)
