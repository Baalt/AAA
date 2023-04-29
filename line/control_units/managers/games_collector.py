import copy

from browser.browser import SmartChromeDriver
from line.analytics.live_dict_builder import LiveDictBuilder
from line.control_units.managers.tasks.game_data_collector import GameCollector
from line.control_units.filters.last_year_filter import LastYearFilter
from utils.error import LiveDictBuilderError


class AllGamesCollector:
    def __init__(self,
                 driver: SmartChromeDriver,
                 schedule_data: dict,
                 all_league_data: dict):

        self.driver = driver
        self.schedule_data = schedule_data
        self.all_league_data = all_league_data
        self.game_number = 0
        self.smart_live_data = {'lst': []}

    def run(self):
        # flag = False
        for full_league_name in self.schedule_data:
            # if 'Australia: FFA Cup' in full_league_name:
            #     flag = True
            if ':' in full_league_name:
                league = full_league_name.split(':')[-1].strip()
                full_league_name = full_league_name.strip()
                # country_league = full_league_name.split(':')[0].strip()
                for game_url in self.schedule_data[full_league_name]['match_url']:
                    self.driver.open_page(game_url)
                    try:
                        game_manager = GameCollector(driver=self.driver, league=league)
                    except AttributeError:
                        continue
                    game_manager.filter_out()

                    try:
                        is_match_data = game_manager.get_match_data()
                    except AttributeError:
                        continue

                    if is_match_data:
                        copy_match_data = copy.deepcopy(game_manager.get_data)
                        last_year_data = LastYearFilter(all_match_data=copy_match_data, all_referee_data=None)
                        last_year_data.filter_home_away_collections('home_collections')
                        last_year_data.filter_home_away_collections('away_collections')

                        self.game_number += 1
                        math_collector = LiveDictBuilder(
                            big_match_data=game_manager.get_data,
                            last_year_data=last_year_data.all_match_data,
                            all_league_data=self.all_league_data[full_league_name],
                            schedule_data=self.schedule_data,
                            league_name=full_league_name,
                            game_number=f"{self.game_number:04d}")
                        try:
                            math_collector.run()
                        except LiveDictBuilderError as e:
                            print('LiveDictBuilderError: ', e)
                            continue
