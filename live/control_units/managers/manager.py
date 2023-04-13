import datetime
from pprint import pprint

from live.analytics.data_analyzer import SmartLiveCompare
from browser.browser import LiveChromeDriver
from live.control_units.managers.schedule import ScheduleManager
from live.control_units.managers.web_crawler import WebCrawler
from telega.telegram_bot import TelegramBot
from telega import config
from toolz.pickle_manager import PickleHandler

if __name__ == '__main__':
    driver = LiveChromeDriver()
    driver.maximize_window()
    driver.open_page('https://www.fon.bet/')

    leagues_dct = PickleHandler().read_data(path_to_file='data/13.04_AllLeaguesData.pkl')
    smart_dict = PickleHandler().read_data(path_to_file='data/13.04_AllTeamsData.pkl')
    browser = ScheduleManager(smart_dict=smart_dict)
    full_smart_dict = browser.run()
    from data.test_data import smrt, lv

    tel = TelegramBot(token=config.token, chat_id=config.chat_id)
    await tel.change_data_and_delete_messages()
    await tel.delete_all_messages()

    slc = SmartLiveCompare(smart_data=smrt, live_data=lv, league_data=leagues_dct, telegram=tel)
    await slc.compare()

    pprint(lv['league'])
    now = datetime.datetime.now()
    while True:
        now_plus_delta = now + datetime.timedelta(minutes=10)
        browser = ScheduleManager(smart_dict=smart_dict)
        full_smart_dict = browser.run()
        operator = WebCrawler(driver=browser.get_driver(), smart_data=full_smart_dict)
        while now_plus_delta > now:
            operator.run_crawler()
            now = datetime.datetime.now()

    # driver = LiveChromeDriver()
    # driver.maximize_window()
    # driver.open_page('https://www.fon.bet/')
    #
    # soup = BeautifulSoup(driver.get_page_html(), 'lxml')
    # scraper = RealTimeGameScraper()
    # scraper.collect_stats(soup=soup, match_stat='corners', total_text='Total corners',
    #                       team_total_text='Team totals corners',
    #                       handicap_text='Сorners handicap')
    # scraper.scrape_match_time(soup=soup)
    # scraper.scrape_league(soup=soup)
    # scraper.scrape_team_names(soup=soup)
    # scraper.scrape_match_score(soup=soup)
    # scraper.scrape_red_cards(soup=soup)
    # scraper.show_game_info()
