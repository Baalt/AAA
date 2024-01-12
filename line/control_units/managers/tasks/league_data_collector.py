import time

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver
from line.control_units.scrapers.league_scraper import LeagueScraper
from utils.stat_switcher import stats_dict


class LeagueDataCollector:

    def __init__(self, driver: SmartChromeDriver):
        self.driver = driver
        self.data = {}

    def show_data(self) -> None:
        from pprint import pprint
        pprint(self.data)

    def get_data(self):
        return self.data

    def scrape_data(self) -> None:
        self.scrape_season('current_season')
        self.driver.driver.refresh()
        try:
            self.driver.buttons.get_previous_season_buttons()[-2].click()
            self.driver.buttons.get_previous_season_buttons()[-1].click()
            self.scrape_season('previous_season')
        except IndexError:
            pass

    def scrape_season(self, season_key: str) -> None:
        self.data[season_key] = {}
        self.scraper = LeagueScraper(data=self.data[season_key])
        for button in self.driver.buttons.get_smart_stats_buttons():
            button.click()
            self.refresh_page()
            self.wait_for_elements()
            time.sleep(1)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])
            except KeyError as err:
                print('I try to catch League xG key err', err)
            break
        # try:
        #     self.handle_button_and_soup('Ауты')
        # except TimeoutException:
        #     # self.click_anywhere_on_page()
        #     self.refresh_page()
        #     self.handle_button_and_soup('Ауты')
        # try:
        #     self.handle_button_and_soup('Удары от ворот')
        # except TimeoutException:
        #     self.refresh_page()
        #     self.handle_button_and_soup('Удары от ворот')
        # try:
        #     self.handle_button_and_soup('Удары')
        # except TimeoutException:
        #     self.refresh_page()
        #     self.handle_button_and_soup('Удары')

    def handle_button_and_soup(self, button_text: str) -> None:
        other_button = self.driver.buttons.get_other_button()
        other_button.click()
        time.sleep(1)
        self.driver.buttons.get_drop_down_button(button_text=button_text).click()
        self.refresh_page()
        self.wait_for_elements()
        time.sleep(1)
        button = self.driver.buttons.get_other_button()
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])

    def refresh_page(self) -> None:
        try:
            self.driver.buttons.get_refresh_button().click()
        except NoSuchElementException:
            pass

    def wait_for_elements(self) -> None:
        WebDriverWait(self.driver.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
