import copy

from selenium.common import ElementClickInterceptedException, NoSuchElementException

from browser.browser import SmartChromeDriver
from line.analytics.live_dict_builder import LiveDictBuilder
from line.control_units.managers.referee_collector import RefereeCollector
from line.control_units.managers.tasks.game_data_collector import GameCollector
from line.control_units.managers.tasks.coeff_data_collector import CoefficientDataManager
from line.control_units.filters.last_year_filter import LastYearFilter
from telega.telegram_bot import TelegramBot
from telega import config
from utils.error import LiveDictBuilderError


class AllGamesCollector:
    def __init__(self,
                 driver: SmartChromeDriver,
                 schedule_data: dict,
                 all_league_data: dict):

        self.driver = driver
        self.telegram = TelegramBot(token=config.token, chat_id=config.chat_id)
        self.schedule_data = schedule_data
        self.all_league_data = all_league_data
        self.game_number = 0
        self.smart_live_data = {'lst': []}

    async def run(self):
        # flag = False
        for full_league_name in self.schedule_data:
            # if 'Brazil: Serie B' in full_league_name:
            #     flag = True
            if ':' in full_league_name:
                league = full_league_name.split(':')[-1].strip()
                full_league_name = full_league_name.strip()
                for game_url in self.schedule_data[full_league_name]['match_url']:
                    self.driver.open_page(game_url)
                    try:
                        game_manager = GameCollector(driver=self.driver, league=league)
                    except AttributeError:
                        continue
                    try:
                        game_manager.filter_out()
                    except ElementClickInterceptedException:
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

                        coeff_manager = CoefficientDataManager(driver=self.driver)
                        coeff_manager.get_coefficients_data()

                        referee_manager = RefereeCollector(driver=self.driver, league=league)
                        try:
                            referee_manager.collect_referee_data()
                            referee_data = referee_manager.scraper.get_data()
                        except NoSuchElementException:
                            referee_data = None

                        self.game_number += 1
                        try:
                            league_data = self.all_league_data[full_league_name]
                        except KeyError as e:
                            print('league_data error:', e)
                            continue
                        math_collector = LiveDictBuilder(
                            telegram=self.telegram,
                            big_match_data=game_manager.get_data,
                            last_year_data=last_year_data.all_match_data,
                            all_league_data=league_data,
                            schedule_data=self.schedule_data,
                            coefficients=coeff_manager.get_data,
                            league_name=full_league_name,
                            referee_data=referee_data,
                            game_number=f"{self.game_number:04d}")
                        try:
                            await math_collector.run()
                        except LiveDictBuilderError as e:
                            print('LiveDictBuilderError: ', e)
                            continue
