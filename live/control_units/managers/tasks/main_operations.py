import re
import time

from selenium.common import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from browser.browser import LiveChromeDriver
from config_smrt import LIVE_SOURCE


class BrowserPreparer:
    def __init__(self, driver: LiveChromeDriver):
        self.browser = driver
        self.browser.maximize_window()

    def open_page(self, url=LIVE_SOURCE):
        self.browser.open_page(url=url)

    def switch_language(self):
        select_language_button = self.browser.buttons.get_language_button()
        select_language_button.click()
        select_english_button = self.browser.buttons.get_english_button()
        select_english_button.click()


class FootballMenuHandler:
    def __init__(self, driver: LiveChromeDriver):
        self.browser = driver
        self.commands_dict = {}

    def get_commands_dict(self):
        return self.commands_dict

    def open_main_football_menu(self):
        select_football_menu = self.browser.buttons.get_football_category_button()
        select_football_menu.click()

    def open_full_leagues_list(self):
        try:
            select_show_all_button = self.browser.buttons.get_show_all_button()
            select_show_all_button.click()
        except NoSuchElementException:
            pass

    def open_all_football_leagues(self):
        while True:
            buttons = self.browser.buttons.get_all_leagues_buttons()
            if not buttons:
                self.scroll_page_down()
                time.sleep(2)
                buttons = self.browser.buttons.get_all_leagues_buttons()
                if not buttons:
                    break
            for button in buttons:
                try:
                    ActionChains(self.browser.driver).move_to_element(button).perform()
                    button.click()
                    self.browser.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", button)
                except (StaleElementReferenceException, ElementClickInterceptedException):
                    pass

                soup = BeautifulSoup(self.browser.get_page_html(), 'lxml')
                self.extract_commands_to_dict(soup)

    def scroll_up(self):
        body = self.browser.driver.find_element(By.CSS_SELECTOR, 'body')
        # Scroll down
        body.send_keys(Keys.HOME)

    # def scroll_up(self):
    #     # Use JavaScript to scroll to the top
    #     self.browser.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_page_down(self):
        body = self.browser.driver.find_element(By.CSS_SELECTOR, 'body')
        # Scroll down
        body.send_keys(Keys.PAGE_DOWN)

    def extract_commands_to_dict(self, soup):
        commands = soup.find_all('a', class_=lambda
            x: x and 'filter-component-row-container' in x and 'filter-item-event-container' in x)
        for pair in commands:
            name = pair.find_next('div').get_text(strip=True)
            href = pair.get('href')
            if name not in self.commands_dict and self.is_valid_name(name=name):
                self.commands_dict[name] = href

    def is_valid_name(self, name):
        return all(x not in name for x in ['(', '-pro']) and re.search('U\d\d', name) is None
