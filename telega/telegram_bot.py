import os
import telegram
from telega import config


class TelegramBot:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    async def send_message_with_files(self, message, *files):
        media = []
        for file in files:
            if os.path.isfile(file):
                media.append(telegram.InputMediaPhoto(open(file, 'rb')))
        if not media:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        else:
            await self.bot.send_media_group(chat_id=self.chat_id, media=media, caption=message)

