import datetime

from selenium.common.exceptions import TimeoutException

from browser.browser import LiveChromeDriver
from live.control_units.managers.schedule import ScheduleManager
from live.control_units.managers.tasks.main_operations import BrowserPreparer
from live.control_units.managers.web_crawler import WebCrawler
from telega.telegram_bot import TelegramBot
from telega import config
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from config_smrt import LIVE_SOURCE


async def run_bot():
    excluded_games = {}
    driver = LiveChromeDriver()
    try:
        line_data = PickleHandler().read_data(path_to_file=f'data/{get_today_date()}_AllLineData.pkl')
        leagues_dct = PickleHandler().read_data(path_to_file=f'data/{get_today_date()}_AllLeaguesData.pkl')
    except FileNotFoundError:
        line_data, leagues_dct = {}, {}
    tel = TelegramBot(token=config.token, chat_id=config.chat_id)
    browser = BrowserPreparer(driver=driver)
    browser.open_page()
    now = datetime.datetime.now()
    while True:
        now_plus_delta = now + datetime.timedelta(minutes=10)
        try:
            browser = ScheduleManager(driver=driver, smart_dict=line_data)
            lv_smrt_dct = browser.run()
        except (TimeoutException, AttributeError):
            continue
        operator = WebCrawler(driver=browser.get_driver(),
                              smart_data=lv_smrt_dct,
                              league_data=leagues_dct,
                              line_data=line_data,
                              tel=tel,
                              excluded_games=excluded_games)
        while now_plus_delta > now:
            await operator.run_crawler()
            # try:
            #     await tel.change_data_and_delete_messages(lv_smrt_data=lv_smrt_dct)
            # except NetworkError as err:
            #     print('change_data_and_delete_messages.ERROR: ', err)
            now = datetime.datetime.now()
        driver.open_page(LIVE_SOURCE)
