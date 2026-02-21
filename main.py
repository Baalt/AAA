import asyncio
import os
import json
import glob
import time
from datetime import date
from pprint import pprint

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.live_scraper import FootballParser, LiveFootballParser  # Импорт OK
from live.control_units.managers.tasks.match_checker import MatchChecker, WeakerMatchChecker
from telega.telegram_bot import TelegramBot
from telega import config


async def run_bot():
    driver = LiveChromeDriver()
    driver.maximize_window()

    # Текущая дата и имена новых файлов
    today = date.today().isoformat()
    favorites_file = f"strong_favorites_{today}.json"
    weaker_file = f"weaker_favorites_{today}.json"

    # Паттерн для ВСЕХ favorites-файлов
    pattern = "*_favorites_*.json"

    # Удаляем старые (кроме сегодняшних)
    for old_file in glob.glob(pattern):
        if old_file not in [favorites_file, weaker_file]:
            try:
                os.remove(old_file)
                print(f"Удалён старый файл: {old_file}")
            except Exception as e:
                print(f"Не удалось удалить {old_file}: {e}")

    # Загрузка или парсинг
    if os.path.exists(favorites_file) and os.path.exists(weaker_file):
        print(f"Загружаем strong_favorites из {favorites_file} и weaker_favorites из {weaker_file}")
        with open(favorites_file, 'r', encoding='utf-8') as f:
            strong_favorites = json.load(f)
        with open(weaker_file, 'r', encoding='utf-8') as f:
            weaker_favorites = json.load(f)
    else:
        print(f"Файлы не найдены. Запускаем парсинг...")
        driver.open_page('https://fon.bet/sports/football?mode=1&dateInterval=7')
        time.sleep(6)

        strong_favorites = {}
        weaker_favorites = {}
        parser = FootballParser(driver, strong_favorites, weaker_favorites)

        with open(favorites_file, 'w', encoding='utf-8') as f:
            json.dump(strong_favorites, f, ensure_ascii=False, indent=4)
        with open(weaker_file, 'w', encoding='utf-8') as f:
            json.dump(weaker_favorites, f, ensure_ascii=False, indent=4)
        print(f"strong_favorites сохранены в {favorites_file}")
        print(f"weaker_favorites (от 1.55+) сохранены в {weaker_file}")
        print(f"Итого: strong={len(strong_favorites)}, weaker={len(weaker_favorites)}")

    tel = TelegramBot(token=config.token, chat_id=config.chat_id)

    # Переходим на live-страницу
    driver.open_page('https://fon.bet/live/football')
    time.sleep(6)

    last_total_matches = None

    while True:
        manager = LiveFootballParser(driver)
        live_matches = manager.get_live_matches()

        # Для strong: только матчи с 'удары в створ' или 'вброс аутов'
        strong_live = {
            k: live_matches[k] for k in live_matches
            if k in strong_favorites and 'stats' in live_matches[k] and
               any(s in live_matches[k]['stats'] for s in ['удары в створ', 'вброс аутов'])
        }
        checker = MatchChecker(strong_favorites, strong_live, tel)
        strong_count, strong_matched = await checker.check_matches()

        # Для weaker: хотя бы 'угловые' или 'удары в створ'
        weaker_live = {
            k: live_matches[k] for k in live_matches
            if k in weaker_favorites and 'stats' in live_matches[k] and
               any(s in live_matches[k]['stats'] for s in ['угловые', 'удары в створ'])
        }
        weaker_checker = WeakerMatchChecker(weaker_favorites, weaker_live, tel)
        weaker_count, weaker_matched = await weaker_checker.check_matches()

        total_matches = strong_count + weaker_count
        if total_matches != last_total_matches:
            if total_matches == 0:
                print("Совпадений матчей не найдено.")
            else:
                print(f"Совпадений strong: {strong_count}, weaker: {weaker_count}")
                if strong_count > 0:
                    print("Strong matched:")
                    pprint(strong_matched)
                if weaker_count > 0:
                    print("Weaker matched:")
                    pprint(weaker_matched)

            last_total_matches = total_matches

        if total_matches == 0:
            time.sleep(60)


if __name__ == '__main__':
    asyncio.run(run_bot())
