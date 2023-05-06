import os
import time

from live.analytics.game_info import GameInfo
from telega.telegram_bot import TelegramBot
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from utils.stat_switcher import stats_dict

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


class SmartLiveCompare():
    def __init__(self, smart_data: dict, live_data: dict, league_data: dict, telegram: TelegramBot):
        self.smart_data = smart_data
        self.live_data = live_data
        self.league_data = league_data
        self.telegram = telegram
        self.files = [
            "graph/data/live_stats.png",
            "graph/data/current_season_points.png",
            "graph/data/previous_season_points.png",
            "graph/data/current_season_stat.png",
            "graph/data/previous_season_stat.png"
        ]

    async def compare(self):
        for statistic in self.live_data:
            if statistic in stats_dict.values():
                try:
                    smart_dct = self.smart_data['smart_data'][statistic]
                    total_under = smart_dct['TU']
                    total_over = smart_dct['TO']
                    total_1_under = smart_dct['TU_1']
                    total_1_over = smart_dct['TO_1']
                    total_2_under = smart_dct['TU_2']
                    total_2_over = smart_dct['TO_2']
                    handicap_1 = smart_dct['H1']
                    handicap_2 = smart_dct['H2']
                except KeyError:
                    continue

                await self.__search_total(statistic=statistic,
                                          statistic_key='totals',
                                          total_under=total_under,
                                          total_over=total_over,
                                          rate_direction='total',
                                          key_under='TU',
                                          key_over='TO')

                await self.__search_total(statistic=statistic,
                                          statistic_key='team1_totals',
                                          total_under=total_1_under,
                                          total_over=total_1_over,
                                          rate_direction='total_1',
                                          key_under='TU_1',
                                          key_over='TO_1')
                await self.__search_total(statistic=statistic,
                                          statistic_key='team2_totals',
                                          total_under=total_2_under,
                                          total_over=total_2_over,
                                          rate_direction='total_2',
                                          key_under='TU_2',
                                          key_over='TO_2')

                await self.__search_handicap(statistic=statistic,
                                             statistic_key='team1_handicaps',
                                             handicap=handicap_1,
                                             rate_direction='handicap_1',
                                             key_handicap='H1')
                await self.__search_handicap(statistic=statistic,
                                             statistic_key='team2_handicaps',
                                             handicap=handicap_2,
                                             rate_direction='handicap_2',
                                             key_handicap='H2')

    async def __search_total(self, statistic, statistic_key,
                             total_under, total_over,
                             rate_direction, key_under, key_over):
        try:
            coeff_box = self.live_data[statistic][statistic_key]
        except KeyError as e:
            # print('SmartLiveCompare.search_total_coeff_box error: ', e)
            return

        for coeff_set in coeff_box:
            try:
                live_total = float(coeff_set['total_number'])
                coeff_under = float(coeff_set['coefficient_under'])
            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue
            if total_under:
                if not isinstance(total_under, float):
                    total_under = float(total_under)
                if live_total >= total_under and coeff_under > 1.65:
                    full_rate_direction = rate_direction + '_under'
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        rate_direction=full_rate_direction,
                        live_total=live_total,
                        live_coeff=coeff_under,
                        smart_total=total_under,
                        key=key_under)
                    self.__plot_graphs(statistic=statistic, key=key_under)
                    message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                    await self.telegram.send_message_with_files(message, *self.files)
                    self.close_the_bet(key=info.get_correction_key())

                try:
                    coeff_over = float(coeff_set['coefficient_over'])
                except KeyError as e:
                    print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                    continue

                if total_over:
                    if not isinstance(total_over, float):
                        total_over = float(total_over)
                    if live_total <= total_over and coeff_over > 1.7:
                        full_rate_direction = rate_direction + '_over'
                        info = GameInfo(
                            live_data=self.live_data,
                            smart_data=self.smart_data,
                            statistic_name=statistic,
                            rate_direction=full_rate_direction,
                            live_total=live_total,
                            live_coeff=coeff_over,
                            smart_total=total_over,
                            key=key_over)
                        self.__plot_graphs(statistic=statistic, key=key_over)
                        message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                        await self.telegram.send_message_with_files(message, *self.files)
                        self.close_the_bet(key=info.get_correction_key())

    async def __search_handicap(self, statistic, statistic_key, handicap, rate_direction, key_handicap):
        try:
            coeff_box = self.live_data[statistic][statistic_key]
        except KeyError as e:
            # print('SmartLiveCompare.search_handicap_engine coeff_box error: ', e)
            return

        for coeff_set in coeff_box:
            try:
                live_handicap = float(coeff_set['total_number'])
                coeff = float(coeff_set['coefficient'])
            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue

            if handicap:
                if not isinstance(handicap, float):
                    handicap = float(handicap)
                if live_handicap >= handicap and coeff > 1.65:
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        live_total=live_handicap,
                        live_coeff=coeff,
                        smart_total=handicap,
                        rate_direction=rate_direction,
                        key=key_handicap)
                    self.__plot_graphs(statistic=statistic, key=key_handicap)
                    message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                    await self.telegram.send_message_with_files(message, *self.files)
                    self.close_the_bet(key=info.get_correction_key())

    def __plot_graphs(self, statistic, key):
        self.delete_files_in_folder(folder_path='graph/data')
        MatchStatsVisualizer(data=self.live_data['match_stats']).plot_bar_chart()
        current_viz = TeamsStatsVisualizer(
            data=self.league_data[self.smart_data['smart_data']['league']]['current_season'],
            team_name_1=self.smart_data['smart_data']['team1_name'],
            team_name_2=self.smart_data['smart_data']['team2_name'])
        current_viz.plot_points(
            data_lst=self.league_data[self.smart_data['smart_data']['league']]['current_season']['goals'],
            season='current_season')
        previous_viz = TeamsStatsVisualizer(
            data=self.league_data[self.smart_data['smart_data']['league']]['previous_season'],
            team_name_1=self.smart_data['smart_data']['team1_name'],
            team_name_2=self.smart_data['smart_data']['team2_name'])
        previous_viz.plot_points(
            data_lst=self.league_data[self.smart_data['smart_data']['league']]['previous_season']['goals'],
            season='previous_season')
        current_viz.plot_team_stats(stat_key=statistic, season='current_season', sort_by='avg_individual_team')
        previous_viz.plot_team_stats(stat_key=statistic, season='previous_season', sort_by='avg_individual_team')
        time.sleep(3)

    def delete_files_in_folder(self, folder_path):
        """
        Deletes all files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)

    def close_the_bet(self, key):
        if key:
            # Split the key by the separator ➠
            parts = key.rstrip('➠').split('➠')
            try:
                self.smart_data['smart_data'][parts[1]][parts[2]] = None
            except KeyError as e:
                print('change smart_data error: ', e)

            file_path = os.path.join("data", f"{get_today_date()}_AllGamesData.pkl")
            handler = PickleHandler()
            if os.path.exists(file_path):
                full_smart_data = handler.read_data(file_path)
                for dct in full_smart_data['lst']:
                    if dct['game_number'] == self.smart_data['smart_data']['game_number']:
                        dct[parts[1]][parts[2]] = None
                        handler.write_data(full_smart_data, file_path)
                        break
            else:
                print(f"File {file_path} not found.")
