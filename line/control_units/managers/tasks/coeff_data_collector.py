import time

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from browser.browser import SmartChromeDriver
from line.control_units.scrapers.coefficient_scraper import CoefficientsScraper


class CoefficientDataManager:
    def __init__(self, driver: SmartChromeDriver):
        self.driver = driver
        self.coefficients_data = {}
        self.scraper = CoefficientsScraper()

    @property
    def get_data(self):
        return self.coefficients_data

    def _create_dict_structure(self, soup: BeautifulSoup):
        self.coefficients_data[self.scraper.get_statistic_name(soup=soup, tooltip=False)] = {
            'total&coefficient': [],
            'total_1_&coefficient': [],
            'total_2_&coefficient': [],
            'handicap_1_&coefficient': [],
            'handicap_2_&coefficient': [],
        }

    def get_coefficients_data(self):
        self.driver.buttons.open_coefficient_button().click()
        try:
            self._wait_for_elements("//table[@class='table-sm table table-bordered matches betting-table text-center']")
            time.sleep(0.5)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self._create_dict_structure(soup=soup)
            self.scraper.get_totals_data(soup=soup, coefficient_data=self.coefficients_data, tooltip=True)
        except TimeoutException:
            pass

        all_buttons = self.driver.buttons.get_smart_stats_buttons()
        buttons = [all_buttons[1]] + all_buttons[2:10]
        for button in buttons:
            button.click()
            self.driver.buttons.get_refresh_button().click()
            try:
                self._wait_for_elements()
                time.sleep(0.5)
            except TimeoutException:
                continue

            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.get_totals_data(soup=soup, coefficient_data=self.coefficients_data)

        self.driver.buttons.coefficient_handicap_button().click()
        buttons = all_buttons[0:2] + all_buttons[2:10]
        for button in buttons:
            button.click()
            self.driver.buttons.get_refresh_button().click()
            try:
                self._wait_for_elements()
                time.sleep(0.5)
            except TimeoutException:
                continue

            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            self.scraper.get_handicap_data(soup=soup, coefficient_data=self.coefficients_data)

    def _wait_for_elements(self, selector="//div[@class='card' and @style='display: none;']"):
        WebDriverWait(self.driver.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, selector)))
