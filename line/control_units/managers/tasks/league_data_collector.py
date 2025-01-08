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
        self.statistic_name = ['Голы', 'Угловые', 'ЖК', 'Офсайды', 'Фолы', 'Уд. в створ', 'Ауты']
        self.scraper = LeagueScraper(data=self.data)

    def show_data(self) -> None:
        from pprint import pprint
        pprint(self.data)

    def get_data(self):
        return self.data

    def scrape_data(self) -> None:
        self.scrape_season()
        self.scrape_referee()

    def scrape_referee(self):
        if self.driver.buttons.check_and_press_referee_button():
            self.wait_for_elements(xpath='//div[@id="table_referee_wrapper"]')
            time.sleep(2)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.scrape_ref_table(soup, key='ref_yellows')
            self.driver.buttons.get_fouls_button().click()
            time.sleep(1)
            self.refresh_page()
            time.sleep(3)
            self.wait_for_elements(xpath='//div[@id="table_referee_wrapper"]')
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.scrape_ref_table(soup, key='ref_fouls')

    def scrape_season(self) -> None:
        time.sleep(2)
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.scrape_league_table(soup=soup, key='goals')
        idx = 1
        for button in self.driver.buttons.get_smart_stats_buttons()[1:]:
            button.click()
            time.sleep(1)
            button.click()
            self.refresh_page()
            self.wait_for_elements()
            time.sleep(3)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_league_table(soup=soup,
                                                 key=stats_dict[
                                                     self.statistic_name[idx]])  # stats_dict[button.text.strip()]
            except KeyError as err:
                print('I try to catch League xG key err', err)
            idx += 1

        try:
            self.handle_button_and_soup('Удары от ворот')
        except TimeoutException:
            self.refresh_page()
            self.handle_button_and_soup('Удары от ворот')
        try:
            self.handle_button_and_soup('Удары')
        except TimeoutException:
            self.refresh_page()
            self.handle_button_and_soup('Удары')

    def handle_button_and_soup(self, button_text: str) -> None:
        other_button = self.driver.buttons.get_other_button()
        other_button.click()
        time.sleep(1)
        self.driver.buttons.get_drop_down_button(button_text=button_text).click()
        self.refresh_page()
        self.wait_for_elements()
        time.sleep(2)
        button = self.driver.buttons.get_other_button()
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.scrape_league_table(soup=soup, key=stats_dict[button.text.strip()])

    def refresh_page(self) -> None:
        try:
            self.driver.buttons.get_refresh_button().click()
        except NoSuchElementException:
            pass

    def wait_for_elements(self, xpath='//*') -> None:
        WebDriverWait(self.driver.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
