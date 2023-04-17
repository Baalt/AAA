import os.path

from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver
from line.control_units.managers.tasks.league_data_collector import LeagueDataCollector
from line.control_units.scrapers.schedule_scraper import ScheduleScraper
from toolz.pickle_manager import PickleHandler
from config_smrt import SOURCE, LOGIN, PASSWORD


class AllLeaguesCollector:
    def __init__(self, driver: SmartChromeDriver, schedule_data: dict):
        self.driver = driver
        self.schedule_data = schedule_data
        self.data_file_name = f"data/{self.schedule_data['date']}_AllLeaguesData.pkl"
        self.data = {}

    def load_data_from_file(self):
        if os.path.exists(self.data_file_name):
            pickle_handler = PickleHandler()
            self.data = pickle_handler.read_data(self.data_file_name)

    def show_data(self):
        self.load_data_from_file()
        from pprint import pprint
        pprint(self.data)

    def get_data(self):
        self.load_data_from_file()
        return self.data

    def scrape_league_data(self, league_key, url):
        self.driver.open_page(url=url)
        league_data_scraper = LeagueDataCollector(driver=self.driver)
        league_data_scraper.scrape_data()
        league_data_scraper.get_data()
        # Add the league data to the existing data
        self.data[league_key] = league_data_scraper.data
        # Save the updated data to the file
        pickle_handler = PickleHandler()
        pickle_handler.write_data(self.data, self.data_file_name)

    def run(self, address):
        self.load_data_from_file()
        # flag = False
        for league_key, league_data in self.schedule_data.items():
            # if 'Brazil: Serie B' in league_key:
            #     flag = True
            if league_key != 'date':
                url = address + league_data['league_url']
                self.scrape_league_data(league_key, url)
        self.driver.close()


if __name__ == '__main__':
    # Collect league data
    driver = SmartChromeDriver()
    driver.maximize_window()
    login_page = SOURCE + '/login'
    driver.open_page(url=login_page)
    driver.login(username=LOGIN, password=PASSWORD)
    input('close add and choose the day')
    soup = BeautifulSoup(driver.get_page_html(), 'lxml')
    scraper = ScheduleScraper(soup=soup)
    scraper.scrape_date_data(soup=soup)
    scraper.scrape_schedule_data(soup=soup)
    collector = AllLeaguesCollector(driver=driver, schedule_data=scraper.get_schedule_data())
    collector.run(address=SOURCE)
