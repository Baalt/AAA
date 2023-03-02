import asyncio

from async_live.control_units.browser.browser import HeadlessChromeDriver
from async_live.control_units.async_manager.tasks.main_operations import BrowserPreparer


class LiveManager:
    def __init__(self):
        self.browser = HeadlessChromeDriver(headless=False)
        self.browser.maximize_window()


    def preparing_browser_for_work(self, url='https://www.fon.bet/live/football/'):
        self.browser.open_page(url=url)


    def run(self):
        controller = BrowserPreparer(browser=self.browser)
        controller.open_page()
        controller.switch_language()
