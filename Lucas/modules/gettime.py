import datetime
from typing import List

import requests
from Lucas import TIME_API_KEY, dispatcher
from Lucas.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"https://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                if zone["dst"] == 1:
                    daylight_saving = "Yes"
                else:
                    daylight_saving = "No"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (
            f"<b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲:</b> <code>{country_name}</code>\n"
            f"<b>𝐙𝐨𝐧𝐞 𝐍𝐚𝐦𝐞:</b> <code>{country_zone}</code>\n"
            f"<b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐂𝐨𝐝𝐞:</b> <code>{country_code}</code>\n"
            f"<b>𝐃𝐚𝐲𝐥𝐢𝐠𝐡𝐭 𝐬𝐚𝐯𝐢𝐧𝐠:</b> <code>{daylight_saving}</code>\n"
            f"<b>𝐃𝐚𝐲:</b> <code>{current_day}</code>\n"
            f"<b>𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐓𝐢𝐦𝐞:</b> <code>{current_time}</code>\n"
            f"<b>𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐃𝐚𝐭𝐞:</b> <code>{current_date}</code>\n"
            '<b>𝐓𝐢𝐦𝐞𝐳𝐨𝐧𝐞𝐬:</b> <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">List here</a>'
        )
    except:
        result = None

    return result


@run_async
def gettime(update: Update, context: CallbackContext):
    message = update.effective_message

    try:
        query = message.text.strip().split(" ", 1)[1]
    except:
        message.reply_text("𝐏𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐜𝐨𝐮𝐧𝐭𝐫𝐲 𝐧𝐚𝐦𝐞/𝐚𝐛𝐛𝐫𝐞𝐯𝐢𝐚𝐭𝐢𝐨𝐧/𝐭𝐢𝐦𝐞𝐳𝐨𝐧𝐞 𝐭𝐨 𝐟𝐢𝐧𝐝.")
        return
    send_message = message.reply_text(
        f"𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐭𝐢𝐦𝐞𝐳𝐨𝐧𝐞 𝐢𝐧𝐟𝐨 𝐟𝐨𝐫 <b>{query}</b>", parse_mode=ParseMode.HTML
    )

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        send_message.edit_text(
            f"𝐓𝐢𝐦𝐞𝐳𝐨𝐧𝐞 𝐢𝐧𝐟𝐨 𝐧𝐨𝐭 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐟𝐨𝐫 <b>{query}</b>\n"
            '<b>𝐀𝐥𝐥 𝐓𝐢𝐦𝐞𝐳𝐨𝐧𝐞𝐬:</b> <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">𝐋𝐢𝐬𝐭 𝐡𝐞𝐫𝐞</a>',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        return

    send_message.edit_text(
        result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


TIME_HANDLER = DisableAbleCommandHandler("time", gettime)

dispatcher.add_handler(TIME_HANDLER)

__mod_name__ = "TIME"
__command_list__ = ["time"]
__handlers__ = [TIME_HANDLER]
