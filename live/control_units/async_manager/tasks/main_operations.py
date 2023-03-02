from async_live.control_units.browser.browser import HeadlessChromeDriver
from async_live.control_units.scripers.schedule_data_collector import ScheduleScraper

class BrowserPreparer:
    def __init__(self, browser: HeadlessChromeDriver):
        self.browser = browser

    def open_page(self, url='https://www.fon.bet/live/football/'):
        self.browser.open_page(url=url)

    def switch_language(self):
        select_language_button = self.browser.buttons.get_select_language_button()
        select_language_button.click()
        select_english_button = self.browser.buttons.get_select_english_button()
        select_english_button.click()

class FootballMenuHandler:
    def __init__(self, browser):
        self.browser = browser

    def open_main_football_menu(self):
        select_football_menu =  self.browser.buttons.get_select_football_category_button()
        select_football_menu.click()

    def open_full_leagues_list(self):
        select_show_all_button = self.browser.buttons.get_select_show_all_button()
        select_show_all_button.click()

    def open_all_football_leagues(self):
        select_all_leagues_buttons = self.browser.buttons.get_select_all_leagues_buttons()
        for button in select_all_leagues_buttons[1:]:
            button.click()


driver = HeadlessChromeDriver(headless=False)
test = BrowserPreparer(browser=driver)
test.browser.maximize_window()
test.open_page()
test.switch_language()
test2 = FootballMenuHandler(browser=driver)
test2.open_main_football_menu()
test2.open_full_leagues_list()
test2.open_all_football_leagues()
# time.sleep(1)
test3 = ScheduleScraper(html=driver.get_page_html())
from pprint import pprint
pprint(test3.extract_commands_to_dict())

