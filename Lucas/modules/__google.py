from bs4 import BeautifulSoup
import urllib
from Lucas import telethn as tbot
import glob
import io
import os
import re
import aiohttp
import urllib.request
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from PIL import Image
from search_engine_parser import GoogleSearch

import bs4
import html2text
from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from Lucas import *

from Lucas.events import register

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern="^/google (.*)")
async def _(event):
    if event.fwd_from:
        return
    
    webevent = await event.reply("searching........")
    match = event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"⚫[{title}]({link})\n**{desc}**\n\n"
        except IndexError:
            break
    await webevent.edit(
        "**𝐒𝐞𝐚𝐫𝐜𝐡 𝐐𝐮𝐞𝐫𝐲 :**\n`" + match + "`\n\n**Results:**\n" + msg, link_preview=False
    )

@register(pattern="^/img (.*)")
async def img_sampler(event):
    if event.fwd_from:
        return
    
    query = event.pattern_match.group(1)
    jit = f'"{query}"'
    downloader.download(
        jit,
        limit=4,
        output_dir="store",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
    )
    os.chdir(f'./store/"{query}"')
    types = ("*.png", "*.jpeg", "*.jpg")  # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    await tbot.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    os.chdir("/app")
    os.system("rm -rf store")


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern=r"^/reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await tbot.download_media(message, photo)
    else:
        await img.reply("`Reply to photo or sticker nigger.`")
        return

    if photo:
        dev = await img.reply("`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await dev.edit("`Unsupported sexuality, most likely.`")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]

        if response != 400:
            await dev.edit(
                "`Image successfully uploaded to Google. Maybe.`"
                "\n`Parsing source now. Maybe.`"
            )
        else:
            await dev.edit("`Google told me to fuck off.`")
            return

        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]

        if guess and imgspage:
            await dev.edit(f"[{guess}]({fetchUrl})\n\n`Looking for this Image...`")
        else:
            await dev.edit("`Can't find this piece of shit.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await tbot.send_file(
                entity=await tbot.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await dev.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "best_guess": ""}

    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if counter < int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks


@register(pattern="^/app (.*)")
async def apk(e):
    
    try:
        app_name = e.pattern_match.group(1)
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        lnk = str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Developer :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Features :</code> <a href='"
            + app_link
            + "'>View in Play Store</a>"
        )
        app_details += "\n\n===> Yone <==="
        await e.reply(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await e.reply("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await e.reply("Exception Occured:- " + str(err))


__mod_name__ = "🔍𝐒𝐞𝐚𝐫𝐜𝐡🔎"

__help__ = """
 ❍ /google <𝐭𝐞𝐱𝐭>*:* 𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐚 𝐠𝐨𝐨𝐠𝐥𝐞 𝐬𝐞𝐚𝐫𝐜𝐡
 ❍ /img <𝐭𝐞𝐱𝐭>*:* 𝐒𝐞𝐚𝐫𝐜𝐡 𝐆𝐨𝐨𝐠𝐥𝐞 𝐟𝐨𝐫 𝐢𝐦𝐚𝐠𝐞𝐬 𝐚𝐧𝐝 𝐫𝐞𝐭𝐮𝐫𝐧𝐬 𝐭𝐡𝐞𝐦\n𝐅𝐨𝐫 𝐠𝐫𝐞𝐚𝐭𝐞𝐫 𝐧𝐨. 𝐨𝐟 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐬𝐩𝐞𝐜𝐢𝐟𝐲 𝐥𝐢𝐦, 𝐅𝐨𝐫 𝐞𝐠: `/img 𝐡𝐞𝐥𝐥𝐨 𝐥𝐢𝐦=𝟏𝟎`
 ❍ /app <𝐚𝐩𝐩𝐧𝐚𝐦𝐞>*:* 𝐒𝐞𝐚𝐫𝐜𝐡𝐞𝐬 𝐟𝐨𝐫 𝐚𝐧 𝐚𝐩𝐩 𝐢𝐧 𝐏𝐥𝐚𝐲 𝐒𝐭𝐨𝐫𝐞 𝐚𝐧𝐝 𝐫𝐞𝐭𝐮𝐫𝐧𝐬 𝐢𝐭𝐬 𝐝𝐞𝐭𝐚𝐢𝐥𝐬.
 ❍ /reverse: 𝐃𝐨𝐞𝐬 𝐚 𝐫𝐞𝐯𝐞𝐫𝐬𝐞 𝐢𝐦𝐚𝐠𝐞 𝐬𝐞𝐚𝐫𝐜𝐡 𝐨𝐟 𝐭𝐡𝐞 𝐦𝐞𝐝𝐢𝐚 𝐰𝐡𝐢𝐜𝐡 𝐢𝐭 𝐰𝐚𝐬 𝐫𝐞𝐩𝐥𝐢𝐞𝐝 𝐭𝐨.
 ❍ /gps <𝐥𝐨𝐜𝐚𝐭𝐢𝐨𝐧>*:* 𝐆𝐞𝐭 𝐠𝐩𝐬 𝐥𝐨𝐜𝐚𝐭𝐢𝐨𝐧.
 ❍ /github <𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞>*:* 𝐆𝐞𝐭 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐚𝐛𝐨𝐮𝐭 𝐚 𝐆𝐢𝐭𝐇𝐮𝐛 𝐮𝐬𝐞𝐫.
 ❍ /country <𝐜𝐨𝐮𝐧𝐭𝐫𝐲 𝐧𝐚𝐦𝐞>*:* 𝐆𝐚𝐭𝐡𝐞𝐫𝐢𝐧𝐠 𝐢𝐧𝐟𝐨 𝐚𝐛𝐨𝐮𝐭 𝐠𝐢𝐯𝐞𝐧 𝐜𝐨𝐮𝐧𝐭𝐫𝐲
 ❍ /imdb <𝐌𝐨𝐯𝐢𝐞 𝐧𝐚𝐦𝐞>*:* 𝐆𝐞𝐭 𝐟𝐮𝐥𝐥 𝐢𝐧𝐟𝐨 𝐚𝐛𝐨𝐮𝐭 𝐚 𝐦𝐨𝐯𝐢𝐞 𝐰𝐢𝐭𝐡 𝐢𝐦𝐝𝐛.𝐜𝐨𝐦
 ❍ 𝐋𝐮𝐜𝐚𝐬 <𝐪𝐮𝐞𝐫𝐲>*:* 𝐋𝐮𝐜𝐚𝐬 𝐚𝐧𝐬𝐰𝐞𝐫𝐬 𝐭𝐡𝐞 𝐪𝐮𝐞𝐫𝐲
  💡𝐄𝐱: `𝐋𝐮𝐜𝐚𝐬 𝐰𝐡𝐞𝐫𝐞 𝐢𝐬 𝐈𝐧𝐝𝐢𝐚?`
"""
