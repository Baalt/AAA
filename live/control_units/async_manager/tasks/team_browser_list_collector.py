import asyncio
from typing import Tuple
from selenium import webdriver

from async_live.control_units.async_manager.tasks.command_matcher import FootballTeamsComparison


class MatchCollector:
    def __init__(self):
        self.filter = FootballTeamsComparison()

    async def collect_matches(self, live_dict: dict, smart_dict: dict,
                              browsers: list, url='https://www.fon.bet/') -> None:
        for live_key, live_value in live_dict.items():
            live_home_name, live_away_name = self._split_command_names(command_names=live_key)
            for smart_data in smart_dict['list']:
                smart_home_name, smart_away_name = smart_data['home_command_name'], smart_data['away_command_name']
                match = self.filter.compare_teams(
                    live_team_1=live_home_name,
                    live_team_2=live_away_name,
                    smart_team_1=smart_home_name,
                    smart_team_2=smart_away_name
                )
                if match:
                    # создать обьект для управления браузером, со сценарием и вычисления, а менеджер уже в свою очередь будет
                    # выполнять алгоритм поиска
                    self._open_browser(browsers, url)

        await asyncio.gather(*browsers)

    def _open_browser(self, browsers: list, url: str) -> None:
        driver = webdriver.Chrome()
        driver.get(url)

    def _split_command_names(self, command_names: str, commands_separator=' — ') -> Tuple[str, str]:
        home_team, away_team = command_names.split(commands_separator)
        return home_team, away_team
