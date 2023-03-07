from live.control_units.manager.tasks.command_matcher import FootballTeamsComparison

from typing import Tuple


class MatchCollector:
    def __init__(self, matches: dict):
        self.filter = FootballTeamsComparison()
        self.matches = matches

    def collect_matches(self, schedule_dict: dict, smart_dict: dict) -> None:
        # Remove any keys from self.matches that are not in live_dict keys
        for match_key in list(self.matches.keys()):
            if match_key not in schedule_dict:
                del self.matches[match_key]

        for live_key, live_value in schedule_dict.items():
            if live_key in self.matches:
                continue
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
                    url = 'https://www.fon.bet' + live_value
                    match_data = {
                        'url': url,
                        'live_team_1': live_home_name,
                        'live_team_2': live_away_name,
                        'smart_data': smart_data
                    }
                    self.matches[live_key] = match_data

    def _split_command_names(self, command_names: str, commands_separator=' — ') -> Tuple[str, str]:
        home_team, away_team = command_names.split(commands_separator)
        return home_team, away_team

    def get_matches(self) -> dict:
        return self.matches
