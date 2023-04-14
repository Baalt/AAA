from browser.browser import LiveChromeDriver
from live.control_units.managers.tasks.main_operations import BrowserPreparer, FootballMenuHandler
from live.control_units.managers.tasks.team_browser_list_collector import MatchCollector
from live.control_units.scrapers.schedule_data_collector import ScheduleScraper


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

        controller_1 = ScheduleScraper(html=self.driver.get_page_html())

        controller_2 = MatchCollector(matches=self.matches)
        controller_2.collect_matches(schedule_dict=controller_1.extract_commands_to_dict(),
                                     smart_dict=self.smart_dict)
        return controller_2.get_matches()

    def get_driver(self):
        return self.driver
