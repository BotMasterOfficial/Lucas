from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
import flag
import html, os
from countryinfo import CountryInfo
from Lucas import telethn as borg
from Lucas.events import register


@register(pattern="^/country (.*)")
async def msg(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    lol = input_str
    country = CountryInfo(lol)
    try:
	    a = country.info()
    except:
	    await event.reply("𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐍𝐨𝐭 𝐀𝐯𝐚𝐢𝐚𝐛𝐥𝐞 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲")
    name = a.get("name")
    bb= a.get("altSpellings")
    hu = ''
    for p in bb:
    	hu += p+",  "
	
    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
	    borders += fk+",  "
	
    call = "" 
    WhAt = a.get("callingCodes")
    for what in WhAt:
	    call+= what+"  "
	
    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
	    currencies += FKer+",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR= PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
      po = iSo.get(hitler)
      iso += po+",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag.flag(nox)

    languages = a.get("languages")
    lMAO=""
    for lmao in languages:
	    lMAO += lmao+",  "

    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom =""
    for jerry in tik:
	    tom+=jerry+",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
	    lanester+=targaryen+",   "

    wiki = a.get("wiki")

    caption = f"""<b><u>𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐆𝐚𝐭𝐡𝐞𝐫𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲</b></u>
<b>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐍𝐚𝐦𝐞:- {name}
𝐀𝐥𝐭𝐞𝐫𝐧𝐚𝐭𝐢𝐯𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠:- {hu}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐀𝐫𝐞𝐚:- {area} square kilometers
𝐁𝐨𝐫𝐝𝐞𝐫𝐬:- {borders}
𝐂𝐚𝐥𝐥𝐢𝐧𝐠 𝐂𝐨𝐝𝐞:- {call}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲'𝐬 𝐂𝐚𝐩𝐢𝐭𝐚𝐥:- {capital}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲'𝐬 𝐂𝐮𝐫𝐫𝐞𝐧𝐜𝐲:- {currencies}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲'𝐬 𝐅𝐥𝐚𝐠:- {okie}
𝐃𝐞𝐦𝐨𝐧𝐲𝐦:- {HmM}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐓𝐲𝐩𝐞:- {EsCoBaR}
𝐈𝐒𝐎 𝐍𝐚𝐦𝐞𝐬:- {iso}
𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞𝐬:- {lMAO}
𝐍𝐚𝐭𝐢𝐯𝐞 𝐍𝐚𝐦𝐞:- {nonive}
𝐏𝐨𝐩𝐮𝐥𝐚𝐭𝐢𝐨𝐧:- {waste}
𝐑𝐞𝐠𝐢𝐨𝐧:- {reg}
𝐒𝐮𝐛 𝐑𝐞𝐠𝐢𝐨𝐧:- {sub}
𝐓𝐢𝐦𝐞 𝐙𝐨𝐧𝐞𝐬:- {tom}
𝐓𝐨𝐩 𝐋𝐞𝐯𝐞𝐥 𝐃𝐨𝐦𝐚𝐢𝐧:- {lanester}
𝐖𝐢𝐤𝐢𝐩𝐞𝐝𝐢𝐚:- {wiki}</b>

𝐆𝐚𝐭𝐡𝐞𝐫𝐞𝐝 𝐁𝐲 𝐋𝐮𝐜𝐚𝐬.</b>
"""
    
    
    await borg.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )
    
    await event.delete()
