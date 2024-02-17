import os
import time

from graph.matrix_stats_viz import ScatterPlotBuilder
from live.analytics.game_info import GameInfo, RedCardInfo, SmartRedCardInfo
from telega.telegram_bot import TelegramBot
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from utils.stat_switcher import stats_dict

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


class RedLiveCompare:
    def __init__(self, live_data: dict, line_data: dict, telegram: TelegramBot, excluded_games: dict, game_key: str):
        self.live_data = live_data
        self.line_data = line_data
        self.telegram = telegram
        self.excluded_games = excluded_games
        self.game_key = game_key
        self.is_yellow_cards = True if 'yellow cards' in self.live_data else None
        self.is_fouls = True if 'fouls' in self.live_data else None

    async def compare(self):
        if self.live_data['red cards'] != '0:0':
            if self.is_fouls and self.excluded_games[self.game_key]['red_foul']:
                await self.red_card_foul_checker()

            if self.is_yellow_cards and self.excluded_games[self.game_key]['red_yellow']:
                await  self.red_card_yellows_checker()

        if self.is_yellow_cards and self.excluded_games[self.game_key]['hand_yellow']:
            await self.yellow_card_handicap_checker(handicap_key='team1_handicaps')
            await self.yellow_card_handicap_checker(handicap_key='team2_handicaps')

    async def yellow_card_handicap_checker(self, handicap_key):
        try:
            coeff_box = self.live_data['yellow cards'][handicap_key]
        except KeyError:
            return

        for coeff_set in coeff_box:
            try:
                live_handicap = float(coeff_set['total_number'])
                coeff = float(coeff_set['coefficient'])
            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue
            if live_handicap > 3.6:
                info = RedCardInfo(
                    live_data=self.live_data,
                    yellow_cards=self.is_yellow_cards,
                    fouls=self.is_fouls)
                message = info.get_yellow_handicap_info(live_handicap=live_handicap, coeff=coeff)
                print(message)
                await self.telegram.send_message_with_files(message)
                self.excluded_games[self.game_key]['hand_yellow'] = None

    async def red_card_yellows_checker(self):
        hand_1, hand_2 = self.get_max_yellows_handicap()
        try:
            red_1, red_2 = self.live_data['red cards'].split(':')
        except ValueError:
            red_1, red_2 = self.live_data['red cards'].split('-')

        if red_1 != '0' and hand_2 and hand_2 > 1.9:
            info = RedCardInfo(
                live_data=self.live_data,
                yellow_cards=self.is_yellow_cards,
                fouls=self.is_fouls,
                yellow_handicap=hand_2)
            message = info.get_game_info()
            print(message)
            await self.telegram.send_message_with_files(message)
            self.excluded_games[self.game_key]['red_yellow'] = None

        elif red_2 != '0' and hand_1 and hand_1 > 1.9:
            info = RedCardInfo(
                live_data=self.live_data,
                yellow_cards=self.is_yellow_cards,
                fouls=self.is_fouls,
                yellow_handicap=hand_1)
            message = info.get_game_info()
            print(message)
            await self.telegram.send_message_with_files(message)
            self.excluded_games[self.game_key]['red_yellow'] = None

    async def red_card_foul_checker(self):
        min_foul_line_total = self.get_min_line_total()
        max_foul_live_total = self.get_max_live_total()
        if min_foul_line_total and max_foul_live_total and max_foul_live_total >= min_foul_line_total:
            info = RedCardInfo(
                live_data=self.live_data,
                yellow_cards=self.is_yellow_cards,
                fouls=self.is_fouls,
                foul_line_total=min_foul_line_total,
                foul_live_total=max_foul_live_total)
            message = info.get_game_info()
            print(message)
            await self.telegram.send_message_with_files(message)
            self.excluded_games[self.game_key]['red_foul'] = None

    def get_min_line_total(self):
        try:
            total_list = [float(data['total_number']) for data in self.line_data[self.game_key]['fouls']['totals']]
            return min(total_list) if total_list else None
        except KeyError:
            print('LINE_DATA_DONT_HAVE_A_FOUL_DATA for', self.game_key)

    def get_max_live_total(self):
        try:
            live_list = [float(data['total_number']) for data in self.live_data['fouls']['totals']]
            return max(live_list) if live_list else None
        except KeyError:
            pass

    def get_max_yellows_handicap(self):
        try:
            hand_1_list = [float(data['total_number']) for data in self.live_data['yellow cards']['team1_handicaps']]
            handicap_1 = max(hand_1_list) if hand_1_list else None
        except KeyError:
            handicap_1 = None
        try:
            hand_2_list = [float(data['total_number']) for data in self.live_data['yellow cards']['team2_handicaps']]
            handicap_2 = max(hand_2_list) if hand_2_list else None
        except KeyError:
            handicap_2 = None
        return handicap_1, handicap_2


class SmartLiveCompare:
    def __init__(self, smart_data: dict, live_data: dict, league_data: dict, telegram: TelegramBot):
        self.smart_data = smart_data
        self.live_data = live_data
        self.league_data = league_data
        self.telegram = telegram
        self.is_yellow_cards = True if 'yellow cards' in self.live_data else None
        self.is_fouls = True if 'fouls' in self.live_data else None
        self.files = [
            "graph/data/live_stats.png",
            "graph/data/current_season_points.png",
            "graph/data/previous_season_points.png",
            "graph/data/year_current_season_stat.png",
            "graph/data/year_previous_season_stat.png",
            "graph/data/current_season_stat.png",
            "graph/data/previous_season_stat.png"
        ]

    async def compare(self):
        if self.is_yellow_cards or self.is_fouls:
            if self.live_data['red cards'] and self.smart_data['smart_data']['check']:
                await self.red_card_rate_checker(yellow_cards=self.is_yellow_cards,
                                                 fouls=self.is_fouls)

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
                    # print('self.smart_dataError', err)
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
                    self.__plot_graphs(statistic=statistic,
                                       live_total=live_total,
                                       rate_direction=key_under)
                    message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                    print(message)
                    await self.telegram.send_message_with_files(message, *self.files)
                    self.close_bet(key=info.get_correction_key())

                # try:
                #     coeff_over = float(coeff_set['coefficient_over'])
                # except KeyError as e:
                #     print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                #     continue
                #
                # if total_over:
                #     if not isinstance(total_over, float):
                #         total_over = float(total_over)
                #     if live_total <= total_over and coeff_over > 1.7:
                #         full_rate_direction = rate_direction + '_over'
                #         info = GameInfo(
                #             live_data=self.live_data,
                #             smart_data=self.smart_data,
                #             statistic_name=statistic,
                #             rate_direction=full_rate_direction,
                #             live_total=live_total,
                #             live_coeff=coeff_over,
                #             smart_total=total_over,
                #             key=key_over)
                #         self.__plot_graphs(statistic=statistic,
                #                            live_total=live_total,
                #                            rate_direction=key_over)
                #         message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                #         print(message)
                #         await self.telegram.send_message_with_files(message, *self.files)
                #         self.close_bet(key=info.get_correction_key())

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
                    self.__plot_graphs(statistic=statistic,
                                       live_total=live_handicap,
                                       rate_direction=key_handicap)
                    message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                    print(message)
                    await self.telegram.send_message_with_files(message, *self.files)
                    self.close_bet(key=info.get_correction_key())

                elif statistic == 'yellow cards' and live_handicap >= 4:
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        live_total=live_handicap,
                        live_coeff=coeff,
                        smart_total=handicap,
                        rate_direction=rate_direction,
                        key=key_handicap)
                    self.__plot_graphs(statistic=statistic,
                                       live_total=live_handicap,
                                       rate_direction=key_handicap)
                    message = '\n'.join([info.get_game_info(), info.get_correction_key()])
                    print(message)
                    await self.telegram.send_message_with_files(message, *self.files)
                    self.close_bet(key=info.get_correction_key())

    def __plot_graphs(self, statistic, live_total, rate_direction):
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
        # current_viz.plot_team_stats(stat_key=statistic, season='current_season', sort_by='avg_individual_team')
        # previous_viz.plot_team_stats(stat_key=statistic, season='previous_season', sort_by='avg_individual_team')
        matrix_viz = ScatterPlotBuilder(matrix_data=self.smart_data['smart_data']['year_matrix_data'])
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='year_current_season')
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='year_previous_season')
        matrix_viz = ScatterPlotBuilder(matrix_data=self.smart_data['smart_data']['big_matrix_data'])
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='current_season')
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='previous_season')
        time.sleep(3)

    def __short_plot_graphs(self):
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
        # current_viz.plot_team_stats(stat_key=statistic, season='current_season', sort_by='avg_individual_team')
        # previous_viz.plot_team_stats(stat_key=statistic, season='previous_season', sort_by='avg_individual_team')
        time.sleep(3)

    async def red_card_rate_checker(self, yellow_cards, fouls):
        if self.live_data['red cards'] != '0:0':
            self.__short_plot_graphs()
            info = SmartRedCardInfo(
                live_data=self.live_data,
                smart_data=self.smart_data,
                yellow_cards=yellow_cards,
                fouls=fouls)
            message = '\n'.join([info.get_game_info(), info.get_correction_key()])
            print(message)
            await self.telegram.send_message_with_files(message, *self.files[:3])
            self.close_bet(key=info.get_correction_key(), red_card=True)

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

    def close_bet(self, key, red_card=False):
        parts = key.rstrip('➠').split('➠')
        if red_card:
            try:
                self.smart_data['smart_data'][parts[1]] = None
            except KeyError as e:
                print('change smart_data error: ', e)
        else:
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
                    if red_card:
                        dct[parts[1]] = None
                    else:
                        dct[parts[1]][parts[2]] = None
                    handler.write_data(full_smart_data, file_path)
                    break
        else:
            print(f"File {file_path} not found.")
