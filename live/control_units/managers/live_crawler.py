import asyncio
import os
import json
import glob
import time
from datetime import date

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.live_scraper import FootballParser, LiveFootballParser
from live.control_units.managers.tasks.match_checker import MatchChecker
from telega.telegram_bot import TelegramBot
from telega import config


async def run_bot():
    driver = LiveChromeDriver()
    driver.maximize_window()

    # Текущая дата и имя нового файла
    today = date.today().isoformat()
    favorites_file = f"strong_favorites_{today}.json"

    # Путь ко всем файлам strong_favorites_*.json
    pattern = "strong_favorites_*.json"

    # Удаляем старые файлы (все, кроме сегодняшнего, если он уже существует)
    for old_file in glob.glob(pattern):
        if old_file != favorites_file:
            try:
                os.remove(old_file)
                print(f"Удалён старый файл: {old_file}")
            except Exception as e:
                print(f"Не удалось удалить {old_file}: {e}")

    # Теперь загружаем или создаём strong_favorites
    if os.path.exists(favorites_file):
        print(f"Загружаем strong_favorites из файла {favorites_file}")
        with open(favorites_file, 'r', encoding='utf-8') as f:
            strong_favorites = json.load(f)
    else:
        print(f"Файл {favorites_file} не найден.")
        driver.open_page('https://fon.bet/sports/football?mode=1&dateInterval=7')
        time.sleep(6)
        strong_favorites = FootballParser(driver, {}).get_matches()

        # Сохраняем в новый файл
        with open(favorites_file, 'w', encoding='utf-8') as f:
            json.dump(strong_favorites, f, ensure_ascii=False, indent=4)
        print(f"strong_favorites сохранены в {favorites_file}")

    # Переходим на live
    driver.open_page('https://fon.bet/live/football')
    time.sleep(6)

    tel = TelegramBot(token=config.token, chat_id=config.chat_id)
    last_matches_count = None

    while True:
        manager = LiveFootballParser(driver, strong_favorites)
        checker = MatchChecker(strong_favorites, manager.get_live_matches(), tel)
        matches_count = await checker.check_matches()

        if matches_count != last_matches_count:
            if matches_count == 0:
                print("Совпадений матчей не найдено.")
            else:
                print(f"Совпадений: {matches_count}")
            last_matches_count = matches_count


if __name__ == '__main__':
    asyncio.run(run_bot())
