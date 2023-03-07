import time

from live.control_units.manager.tasks.async_tab_opener import MultipleTabsOpener
from browser.browser import HeadlessChromeDriver
from live.control_units.manager.tasks.main_operations import BrowserPreparer, FootballMenuHandler
from live.control_units.scripers.schedule_data_collector import ScheduleScraper
from live.control_units.manager.tasks.team_browser_list_collector import MatchCollector
from toolz.pickle_manager import PickleHandler

class ScheduleManager:
    def __init__(self, smart_dict: dict):
        self.driver = HeadlessChromeDriver(headless=False)
        self.driver.maximize_window()
        self.matches = {}
        self.smart_dict = smart_dict

    def run(self):
        controller_1 = BrowserPreparer(driver=self.driver)
        controller_1.open_page()
        controller_1.switch_language()

        controller_2 = FootballMenuHandler(driver=self.driver)
        controller_2.open_main_football_menu()
        controller_2.open_full_leagues_list()
        controller_2.open_all_football_leagues()

        controller_3 = ScheduleScraper(html=self.driver.get_page_html())

        controller_4 = MatchCollector(matches=self.matches)
        controller_4.collect_matches(schedule_dict=controller_3.extract_commands_to_dict(),
                                     smart_dict=self.smart_dict)
        return controller_4.get_matches()

class TabSwitcher:
    def __init__(self, driver: HeadlessChromeDriver):
        self.driver = driver

    def switch_tabs(self):
        for handle in self.driver.driver.window_handles:
            self.driver.driver.switch_to.window(handle)
            match_button = self.driver.buttons.get_match_button()
            match_button.click()
            stats_button = self.driver.buttons.get_stats_button()
            stats_button.click()
            time.sleep(4)



if __name__ == '__main__':
    smart_dict = PickleHandler().read_data()
    full_smart_dict = ScheduleManager(smart_dict=smart_dict).run()
    driver = MultipleTabsOpener(driver=HeadlessChromeDriver(headless=False),
                                smart_dict=full_smart_dict)
    await driver.open_all_urls(browser_preparer=BrowserPreparer)
    TabSwitcher(driver=driver.get_driver()).switch_tabs()