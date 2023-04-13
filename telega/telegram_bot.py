import os
import telegram
from toolz.func import get_today_date
from toolz.pickle_manager import PickleHandler


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

    async def change_data_and_delete_messages(self):
        try:
            updates = await self.bot.get_updates()
        except telegram.error.BadRequest:
            return

        for update in updates:
            message = update.message
            if message is not None:
                parts = message.text.rstrip('➠').split('➠')
                file_path = os.path.join("data", f"{get_today_date()}_AllTeamsData.pkl")
                handler = PickleHandler()
                if len(parts) == 4 and os.path.exists(file_path):
                    full_smart_data = handler.read_data(file_path)
                    for dct in full_smart_data['lst']:
                        if dct['game_number'] == parts[0]:
                            dct[parts[1]][parts[2]] = parts[3]
                            handler.write_data(full_smart_data, file_path)

                try:
                    await self.bot.delete_message(chat_id=self.chat_id, message_id=message.message_id)
                except telegram.error.BadRequest:
                    pass

    async def delete_all_messages(self):
        try:
            offset = None
            while True:
                updates = await self.bot.get_updates(offset=offset, timeout=10)
                if not updates:
                    break
                for update in updates:
                    if update.message:
                        offset = updates[-1].update_id + 1
        except telegram.error.TelegramError:
            pass
