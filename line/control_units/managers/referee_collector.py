import time

from selenium.common import ElementClickInterceptedException
from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver
from line.control_units.scrapers.referee_scraper import RefereeScraper


class RefereeCollector:
    def __init__(self, driver: SmartChromeDriver, league: str):
        self.driver = driver
        self.league = league
        self.scraper = RefereeScraper()

    def collect_referee_data(self):
        is_referee_button = self.driver.buttons.check_and_press_referee_button()
        if is_referee_button:
            try:
                self.filter_out()
            except ElementClickInterceptedException:
                self.filter_out()

            self.driver.buttons.get_smart_stats_buttons()[0].click()
            self.driver.buttons.get_refresh_button().click()
            time.sleep(2)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_table(soup, 'ЖК')
            except AttributeError:
                pass
            self.driver.buttons.get_smart_stats_buttons()[4].click()
            self.driver.buttons.get_refresh_button().click()
            time.sleep(2)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_table(soup, 'Фолы')
            except AttributeError:
                pass

    def filter_out(self):
        self.driver.buttons.filter_table_by_matches()
        self.driver.buttons.click_all_league_button()
        self.driver.buttons.click_current_league_button(league=self.league)
        self.driver.buttons.click_all_season_button()


if __name__ == '__main__':
    driver = SmartChromeDriver()
    driver.maximize_window()
    collector = RefereeCollector(driver=driver, league='La Liga')
    collector.collect_referee_data()
