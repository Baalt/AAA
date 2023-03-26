from browser.browser import LiveChromeDriver
from live.control_units.managers.tasks.main_operations import BrowserPreparer, FootballMenuHandler
from live.control_units.managers.tasks.team_browser_list_collector import MatchCollector
from live.control_units.scripers.schedule_data_collector import ScheduleScraper


class ScheduleManager:
    def __init__(self, smart_dict: dict):
        self.driver = LiveChromeDriver(headless=False)
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

    def get_driver(self):
        return self.driver
