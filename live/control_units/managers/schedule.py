import time

from live.control_units.managers.tasks.main_operations import FootballMenuHandler
from live.control_units.managers.tasks.team_browser_list_collector import MatchCollector


class ScheduleManager:
    def __init__(self, driver, smart_dict: dict):
        self.driver = driver
        self.matches = {}
        self.smart_dict = smart_dict

    def run(self):
        controller = FootballMenuHandler(driver=self.driver)
        time.sleep(1)
        controller.open_main_football_menu()
        time.sleep(1)
        controller.open_full_leagues_list()
        time.sleep(1)
        controller.open_all_football_leagues()
        controller.scroll_up()
        time.sleep(1)
        controller.open_all_football_leagues()

        controller_2 = MatchCollector(matches=self.matches)
        controller_2.collect_matches(schedule_dict=controller.get_commands_dict(),
                                     smart_dict=self.smart_dict)
        return controller_2.get_matches()

    def get_driver(self):
        return self.driver
