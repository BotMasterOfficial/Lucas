from telethon.tl.types import InputMediaDice

from Lucas.events import register


@register(pattern="^/dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice(""))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")
    
    else:
        try:
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))
        except BaseException:
            pass


@register(pattern="^/dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🎯"))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")
    
    else:
        try:
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except BaseException:
            pass


@register(pattern="^/ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🏀"))
    input_int = int(input_str)
    if input_int > 5:
        await event.reply("hey nigga use number 1 to 6 only")
    
    else:
        try:
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except BaseException:
            pass



__help__ = """
*𝐏𝐥𝐚𝐲 𝐆𝐚𝐦𝐞 𝐖𝐢𝐭𝐡 𝐄𝐦𝐨𝐣𝐢𝐬:*
- /dice 𝐨𝐫 /𝐝𝐢𝐜𝐞 𝟏 𝐭𝐨 𝟔 𝐚𝐧𝐲 𝐯𝐚𝐥𝐮𝐞
- /ball 𝐨𝐫 /𝐛𝐚𝐥𝐥 𝟏 𝐭𝐨 𝟓 𝐚𝐧𝐲 𝐯𝐚𝐥𝐮𝐞
- /dart 𝐨𝐫 /𝐝𝐚𝐫𝐭 𝟏 𝐭𝐨 𝟔 𝐚𝐧𝐲 𝐯𝐚𝐥𝐮𝐞
𝐔𝐬𝐚𝐠𝐞: 𝐡𝐚𝐡𝐚𝐡𝐚 𝐣𝐮𝐬𝐭 𝐚 𝐦𝐚𝐠𝐢𝐜.
𝐰𝐚𝐫𝐧𝐢𝐧𝐠: 𝐲𝐨𝐮 𝐰𝐨𝐮𝐥𝐝 𝐛𝐞 𝐢𝐧 𝐭𝐫𝐨𝐮𝐛𝐥𝐞 𝐢𝐟 𝐲𝐨𝐮 𝐢𝐧𝐩𝐮𝐭 𝐚𝐧𝐲 𝐨𝐭𝐡𝐞𝐫 𝐯𝐚𝐥𝐮𝐞 𝐭𝐡𝐚𝐧 𝐦𝐞𝐧𝐭𝐢𝐨𝐧𝐞𝐝.
"""

__mod_name__ = "🎮𝐆𝐚𝐦𝐞🎮"
