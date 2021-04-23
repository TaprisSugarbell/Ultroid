# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


import asyncio
import os
import re
import time

from pyUltroid.functions.all import *
from telethon import Button
from telethon.errors import UserNotParticipantError
from telethon.tl.types import DocumentAttributeAudio
from telethon.tl.types import InputWebDocument as wb
from youtubesearchpython import VideosSearch

ytt = "https://telegra.ph/file/afd04510c13914a06dd03.jpg"


@in_pattern("yt")
@in_owner
async def _(event):
    try:
        string = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        fuk = event.builder.article(
            title="Busca algo",
            thumb=wb(ytt, 0, "image/jpeg", []),
            text="**YᴏᴜTᴜʙᴇ Sᴇᴀʀᴄʜ**\n\nNo has buscado nada",
            buttons=Button.switch_inline(
                "Buscar de nuevo",
                query="yt ",
                same_peer=True,
            ),
        )
        await event.answer([fuk])
        return
    results = []
    search = VideosSearch(string, limit=10)
    nub = search.result()
    nibba = nub["result"]
    for v in nibba:
        link = v["link"]
        title = v["title"]
        ids = v["id"]
        duration = v["duration"]
        thumb = f"https://img.youtube.com/vi/{ids}/hqdefault.jpg"
        text = f"**•Título•** `{title}`\n\n**••[Link]({link})••**\n\n**••Duración••** `{duration}`\n\n\n"
        desc = f"Título : {title}\nDuración : {duration}"
        results.append(
            await event.builder.document(
                file=thumb,
                title=title,
                description=desc,
                text=text,
                include_media=True,
                buttons=[
                    [
                        Button.inline("Audio", data=f"audio{link}"),
                        Button.inline("Video", data=f"video{link}"),
                    ],
                    [
                        Button.switch_inline(
                            "Busca de Nuevo",
                            query="yt ",
                            same_peer=True,
                        ),
                        Button.switch_inline(
                            "Compartir",
                            query=f"yt {string}",
                            same_peer=False,
                        ),
                    ],
                ],
            ),
        )
    await event.answer(results)


@callback(re.compile("audio(.*)"))
@owner
async def _(sur):
    url = sur.pattern_match.group(1).decode("UTF-8")
    sur.sender_id
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    song = True
    ytdl_data = await dler(sur, opts, url)
    jpg = f"{ytdl_data['id']}.mp3.jpg"
    png = f"{ytdl_data['id']}.mp3.png"
    webp = f"{ytdl_data['id']}.mp3.webp"
    dir = os.listdir()

    if jpg in dir:
        thumb = jpg
    elif png in dir:
        thumb = png
    elif webp in dir:
        thumb = webp
    else:
        thumb = None

    c_time = time.time()
    if song:
        await sur.edit(
            f"`Preparando la subida de la canción:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*",
        )
        MSG = f"**{ytdl_data['title']}** Subida con éxito !"
        chat = sur.chat_id
        whome = ultroid_bot
        if sur.is_private and sur.sender_id != ultroid_bot.uid:
            chat = sur.sender_id
            whome = asst
            MSG += f"\nConseguir en {Var.BOT_USERNAME}"
        try:
            await whome.send_file(
                chat,
                f"{ytdl_data['id']}.mp3",
                thumb=thumb,
                caption=f"**{ytdl_data['title']}\n{time_formatter((ytdl_data['duration'])*1000)}\n{ytdl_data['uploader']}**",
                supports_streaming=True,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(ytdl_data["duration"]),
                        title=str(ytdl_data["title"]),
                        performer=str(ytdl_data["uploader"]),
                    ),
                ],
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        sur,
                        c_time,
                        "Subiendo..",
                        f"{ytdl_data['title']}.mp3",
                    ),
                ),
            )
        except UserNotParticipantError:
            await asst.send_file(
                sur.sender_id,
                f"{ytdl_data['id']}.mp3",
                thumb=thumb,
                caption=f"**{ytdl_data['title']}\n{time_formatter((ytdl_data['duration'])*1000)}\n{ytdl_data['uploader']}**",
                supports_streaming=True,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(ytdl_data["duration"]),
                        title=str(ytdl_data["title"]),
                        performer=str(ytdl_data["uploader"]),
                    ),
                ],
            )
        os.system(f"rm {ytdl_data['id']}.mp*")
        await sur.edit(
            MSG,
            buttons=Button.switch_inline("Buscar más", query="yt ", same_peer=True),
        )


@callback(re.compile("video(.*)"))
@owner
async def _(fuk):
    url = fuk.pattern_match.group(1).decode("UTF-8")
    fuk.sender_id
    event = fuk
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    video = True
    ytdl_data = await dler(fuk, opts, url)

    c_time = time.time()
    if video:
        await fuk.edit(
            f"`Preparando la subida del vídeo:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*",
        )
        MSG = f"**{ytdl_data['title']}** Subida con éxito !"
        chat = fuk.chat_id
        whome = ultroid_bot
        if event.is_private and event.sender_id != ultroid_bot.uid:
            chat = fuk.sender_id
            whome = asst
            MSG += f"\nConseguir en {Var.BOT_USERNAME}"
        try:
            await whome.send_file(
                chat,
                f"{ytdl_data['id']}.mp4",
                thumb=f"./resources/extras/sayu.jpg",
                caption=f"**{ytdl_data['title']}\n{time_formatter((ytdl_data['duration'])*1000)}\n{ytdl_data['uploader']}**",
                supports_streaming=True,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        fuk,
                        c_time,
                        "Subiendo..",
                        f"{ytdl_data['title']}.mp4",
                    ),
                ),
            )
        except UserNotParticipantError:
            await asst.send_file(
                chat,
                f"{ytdl_data['id']}.mp4",
                thumb=f"./resources/extras/sayu.jpg",
                caption=f"**{ytdl_data['title']}\n{time_formatter((ytdl_data['duration'])*1000)}\n{ytdl_data['uploader']}**",
                supports_streaming=True,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        fuk,
                        c_time,
                        "Subiendo..",
                        f"{ytdl_data['title']}.mp4",
                    ),
                ),
            )
        os.remove(f"{ytdl_data['id']}.mp4")
        await fuk.edit(
            MSG,
            buttons=Button.switch_inline("Buscar más", query="yt ", same_peer=True),
        )
