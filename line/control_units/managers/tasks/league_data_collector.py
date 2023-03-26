from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver
from line.control_units.scrapers.league_scraper import LeagueScraper
from data.football_statistics_translation import stats_dict


class LeagueDataCollector:

    def __init__(self, driver: SmartChromeDriver):
        self.driver = driver
        self.data = {}

    def show_data(self):
        from pprint import pprint
        pprint(self.data)

    def scrape_data(self):
        self.data['current_season'] = {}
        self.scraper = LeagueScraper(data=self.data['current_season'])
        for button in self.driver.buttons.get_smart_stats_buttons():
            button.click()
            try:
                self.driver.buttons.get_refresh_button().click()
            except NoSuchElementException:
                pass
            self.wait_for_elements()
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])

        self.driver.buttons.get_other_button().click()
        self.driver.buttons.get_drop_down_button(button_text='Удары от ворот').click()
        self.driver.buttons.get_refresh_button().click()
        self.wait_for_elements()

        button = self.driver.buttons.get_other_button()
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])

        self.driver.driver.refresh()

        self.driver.buttons.get_previous_season_buttons()[-2].click()
        self.driver.buttons.get_previous_season_buttons()[-1].click()
        self.driver.buttons.get_refresh_button().click()


        self.data['previous_season'] = {}
        self.scraper = LeagueScraper(data=self.data['previous_season'])
        for button in self.driver.buttons.get_smart_stats_buttons():
            button.click()
            try:
                self.driver.buttons.get_refresh_button().click()
            except NoSuchElementException:
                pass
            self.wait_for_elements()
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])

        self.driver.buttons.get_other_button().click()
        self.driver.buttons.get_drop_down_button(button_text='Удары от ворот').click()
        self.driver.buttons.get_refresh_button().click()
        self.wait_for_elements()

        button = self.driver.buttons.get_other_button()
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.from_soup(soup=soup, key=stats_dict[button.text.strip()])


    def wait_for_elements(self):
        WebDriverWait(self.driver.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))


if __name__ == '__main__':
    driver = SmartChromeDriver()
    driver.maximize_window()
    driver.open_page('https://smart-tables.ru')
    driver.login(username='enjoylifebalt@gmail.com', password='astraSTb00rato')

    collector = LeagueDataCollector(driver=driver)
    collector.scrape_data()
    collector.show_data()
