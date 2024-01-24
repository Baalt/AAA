import datetime

from selenium.common.exceptions import TimeoutException
from telegram.error import NetworkError

from browser.browser import LiveChromeDriver
from live.control_units.managers.schedule import ScheduleManager
from live.control_units.managers.tasks.main_operations import BrowserPreparer
from live.control_units.managers.web_crawler import WebCrawler
from telega.telegram_bot import TelegramBot
from telega import config
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from config_smrt import LIVE_SOURCE

if __name__ == '__main__':
    driver = LiveChromeDriver()
    browser = BrowserPreparer(driver=driver)
    browser.open_page()
    browser.switch_language()
    try:
        leagues_dct = PickleHandler().read_data(path_to_file=f'data/{get_today_date()}_AllLeaguesData.pkl')
        smart_dict = PickleHandler().read_data(path_to_file=f'data/{get_today_date()}_AllGamesData.pkl')
    except FileNotFoundError:
        leagues_dct, smart_dict = {}, {}
    tel = TelegramBot(token=config.token, chat_id=config.chat_id)
    now = datetime.datetime.now()
    excluded_red_games = []
    while True:
        now_plus_delta = now + datetime.timedelta(minutes=10)
        try:
            browser = ScheduleManager(driver=driver, smart_dict=smart_dict)
            lv_smrt_dct = browser.run()
        except TimeoutException:
            continue
        print(f'number of scanned smart games {len(lv_smrt_dct.keys())}')
        operator = WebCrawler(driver=browser.get_driver(),
                              smart_data=lv_smrt_dct,
                              league_data=leagues_dct,
                              tel=tel,
                              excluded_red_games=excluded_red_games)
        while now_plus_delta > now:
            await operator.run_crawler()
            try:
                await tel.change_data_and_delete_messages(lv_smrt_data=lv_smrt_dct)
            except NetworkError as err:
                print('change_data_and_delete_messages.ERROR: ', err)
            now = datetime.datetime.now()
        driver.open_page(LIVE_SOURCE)