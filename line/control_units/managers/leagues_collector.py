import os.path

from browser.browser import SmartChromeDriver
from line.control_units.managers.tasks.league_data_collector import LeagueDataCollector
from utils.pickle_manager import PickleHandler


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
