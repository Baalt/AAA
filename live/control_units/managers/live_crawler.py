import asyncio
import time
from pprint import pprint

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.live_scraper import FootballParser, LiveFootballParser
from live.control_units.managers.tasks.match_checker import MatchChecker
from telega.telegram_bot import TelegramBot
from telega import config


async def run_bot():
    driver = LiveChromeDriver()
    driver.maximize_window()
    driver.open_page('https://fon.bet/sports/football?mode=1&dateInterval=6')
    time.sleep(3)

    matches_dict = {}
    strong_favorites = FootballParser(driver, matches_dict).get_matches()
    driver.open_page('https://fon.bet/live/football')
    time.sleep(3)
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
