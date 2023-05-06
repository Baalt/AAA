from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver
from line.control_units.scrapers.schedule_scraper import ScheduleScraper
from line.control_units.managers.leagues_collector import AllLeaguesCollector
from line.control_units.managers.games_collector import AllGamesCollector
from utils.pickle_manager import PickleHandler
from config_smrt import SOURCE, LOGIN, PASSWORD

if __name__ == '__main__':
    driver = SmartChromeDriver()
    driver.maximize_window()
    login_page = SOURCE + '/login'
    driver.open_page(url=login_page)
    driver.login(username=LOGIN, password=PASSWORD)
    input('close add and choose the day')
    soup = BeautifulSoup(driver.get_page_html(), 'lxml')
    scraper = ScheduleScraper(soup=soup)
    scraper.scrape_date(soup=soup)
    scraper.scrape_schedule(soup=soup)
    schedule_data = scraper.get_schedule_data()

    collector = AllLeaguesCollector(driver=driver, schedule_data=scraper.get_schedule_data())
    collector.run(address=SOURCE)

    all_league_data = PickleHandler().read_data(f"data/{schedule_data['date']}_AllLeaguesData.pkl")
    collector = AllGamesCollector(driver=driver,
                                  schedule_data=scraper.get_schedule_data(),
                                  all_league_data=all_league_data)
    await collector.run()
    driver.close()
    all_games_data = PickleHandler().read_data(f"data/{schedule_data['date']}_AllGamesData.pkl")
    print('count of preparing game - ', len(all_games_data['lst']))
