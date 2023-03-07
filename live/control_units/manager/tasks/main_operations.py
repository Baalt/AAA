from selenium.common import StaleElementReferenceException

from browser.browser import HeadlessChromeDriver


class BrowserPreparer:
    def __init__(self, driver: HeadlessChromeDriver):
        self.browser = driver

    def open_page(self, url='https://www.fon.bet/live/football/'):
        self.browser.open_page(url=url)

    def switch_language(self):
        select_language_button = self.browser.buttons.get_language_button()
        select_language_button.click()
        select_english_button = self.browser.buttons.get_english_button()
        select_english_button.click()


class FootballMenuHandler:
    def __init__(self, driver):
        self.browser = driver

    def open_main_football_menu(self):
        select_football_menu = self.browser.buttons.get_football_category_button()
        select_football_menu.click()

    def open_full_leagues_list(self):
        select_show_all_button = self.browser.buttons.get_show_all_button()
        select_show_all_button.click()

    def open_all_football_leagues(self):
        select_all_leagues_buttons = self.browser.buttons.get_all_leagues_buttons()
        for button in select_all_leagues_buttons[1:]:
            try:
                button.click()
            except StaleElementReferenceException:
                continue
