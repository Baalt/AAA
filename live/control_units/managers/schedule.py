import time

from browser.browser import LiveChromeDriver
from live.control_units.managers.tasks.main_operations import BrowserPreparer, FootballMenuHandler
from live.control_units.managers.tasks.team_browser_list_collector import MatchCollector, LineMatchCollector
from live.control_units.scrapers.schedule_data_collector import LiveScheduleScraper


class ScheduleManager:
    def __init__(self, driver, smart_dict: dict):
        self.driver = driver
        self.matches = {}
        self.smart_dict = smart_dict

    def run(self):
        controller = FootballMenuHandler(driver=self.driver)
        controller.open_main_football_menu()
        controller.open_full_leagues_list()
        controller.open_all_football_leagues()

        controller_1 = LiveScheduleScraper(html=self.driver.get_page_html())
        controller_2 = MatchCollector(matches=self.matches)
        controller_2.collect_matches(schedule_dict=controller_1.extract_commands_to_dict(),
                                     smart_dict=self.smart_dict)
        return controller_2.get_matches()

    def get_driver(self):
        return self.driver


class LineScheduleManager:
    def __init__(self, driver: LiveChromeDriver, smart_schedule: list):
        self.driver = driver
        self.matches = {}
        self.smart_schedule = smart_schedule

    def run(self):
        self.driver.buttons.get_pre_match_button().click()
        time.sleep(2)
        controller = FootballMenuHandler(driver=self.driver)
        controller.open_main_football_menu()
        controller.open_full_leagues_list()
        controller.open_all_football_leagues()

        controller_1 = LiveScheduleScraper(html=self.driver.get_page_html())
        from pprint import pprint
        pprint(controller_1.extract_commands_to_dict())
        # controller_2 = LineMatchCollector(smart_schedule=self.smart_schedule,
        #                                   live_schedule=controller_1.extract_commands_to_dict())
