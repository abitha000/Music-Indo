#
# Copyright (C) 2024 by AnonymousX888@Github, < https://github.com/AnonymousX888 >.
#
# This file is part of < https://github.com/hakutakaid/Music-Indo.git > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/Music-Indo.git/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
from datetime import datetime

from pyrogram.enums import ChatType

import config
from MusicIndo import app
from MusicIndo.core.call import Yukki, autoend
from MusicIndo.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from MusicIndo.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if chat_id not in [
                                config.LOG_GROUP_ID,
                                -1002159045835,
                                -1002146211959,
                            ]:
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                    except:
                                        continue
                except:
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await Yukki.stop_stream(chat_id)
                except:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "Bᴏᴛ ʜᴀs ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴅᴜᴇ ᴛᴏ ɪɴᴀᴄᴛɪᴠɪᴛʏ ᴛᴏ ᴀᴠᴏɪᴅ ᴏᴠᴇʀʟᴏᴀᴅ ᴏɴ sᴇʀᴠᴇʀs. Nᴏ-ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.",
                    )
                except:
                    continue


asyncio.create_task(auto_end())
