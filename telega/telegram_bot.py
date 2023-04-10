import asyncio
import telegram
from telega import info

import os
import telegram

class TelegramBot:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def send_images(self):
        image_dir = 'graph/data'
        image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f.endswith('.png')]
        if not image_files:
            return
        for image_file in image_files:
            with open(os.path.join(image_dir, image_file), 'rb') as f:
                self.bot.send_photo(chat_id=self.chat_id, photo=f)


if __name__ == '__main__':
    bot = TelegramBot(token=info.token, chat_id=info.chat_id)
    bot.send_images()

