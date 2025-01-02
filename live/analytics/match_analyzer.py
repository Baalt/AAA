import os
import time
import math

from graph.matrix_stats_viz import ScatterPlotBuilder
from live.analytics.game_info import GameInfo, Info
from telega.telegram_bot import TelegramBot
from utils.error import QuantityError
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from utils.stat_switcher import stats_dict

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


class MatchAnalyzer:
    def __init__(self, info_dict, market, excluded_games, game_key, tel):
        self.info_dict = info_dict
        self.market = market
        self.game_key = game_key
        self.excluded_games = excluded_games
        self.telegram = tel

        self.match_score = info_dict['match_score']
        self.match_time = info_dict['match_time']
        self.team1_name = self._get_or_update_excluded_game('team1_name')
        self.team2_name = self._get_or_update_excluded_game('team2_name')
        self.total_teams = self._get_or_update_excluded_game('total_teams')
        self.tournament_info = self._get_or_update_excluded_game('tournament_info')

        self.team1_info = None
        self.team2_info = None

        self.__assign_teams()
        self.check_quantity_games(quantity=7)

    def _get_or_update_excluded_game(self, key):
        if key in self.info_dict and self.info_dict[key]:
            result = self.info_dict[key]
            self.excluded_games[self.game_key].setdefault(key, result)
            return result
        else:
            return self.excluded_games[self.game_key][key]

    def __assign_teams(self):
        for team_info in self.tournament_info:
            if team_info['name'] == self.team1_name:
                self.team1_info = team_info
            elif team_info['name'] == self.team2_name:
                self.team2_info = team_info

    async def search(self):
        if self.market['yellow_market'] and self.excluded_games[self.game_key]['yellow cards']:
            self.set_values(key='yellow cards')
        if self.market['foul_market'] and self.excluded_games[self.game_key]['fouls']:
            self.set_values(key='fouls')

        if self.excluded_games[self.game_key]['fouls_line'] and self.is_best_rank_range():
            await self.foul_line_message()
        else:
            self.excluded_games[self.game_key]['fouls_line'] = None

        if self.market['yellow_market'] and self.excluded_games[self.game_key]['yellow cards']:
            if self.check_max_match_time(self.match_time, max_minute=75):
                await self.check_and_compare('yellow cards')
            else:
                self.excluded_games[self.game_key]['yellow cards'] = None

        if self.market['foul_market'] and self.excluded_games[self.game_key]['fouls']:
            if self.check_max_match_time(self.match_time, max_minute=75):
                await self.check_and_compare('fouls')
            else:
                self.excluded_games[self.game_key]['fouls'] = None

        if self.market['throw_market'] and self.excluded_games[self.game_key]['throws']:
            await self.analyze_throws()

    async def foul_line_message(self):
        if self.market['foul_market'] and self.excluded_games[self.game_key]['fouls_line']:
            if not ':' in self.match_time or self.check_max_match_time(self.match_time, max_minute=13):
                await self._process_and_send_message(text='LINE FOULS LOOK REF AND TEAMS')
                self.excluded_games[self.game_key]['fouls_line'] = None
            else:
                self.excluded_games[self.game_key]['fouls_line'] = None

    async def analyze_throws(self):
        score1, score2 = map(int, self.info_dict['match_score'].split(':'))
        team1_rank = int(self.team1_info['rank'])
        team2_rank = int(self.team2_info['rank'])

        if self.check_max_match_time(self.match_time, max_minute=81):
            if team1_rank < team2_rank and score1 < score2:
                await self._process_and_send_message(text='LIVE THROWS FAST')
                self.excluded_games[self.game_key]['throws'] = None
            elif team1_rank > team2_rank and score1 > score2:
                await self._process_and_send_message(text='LIVE THROWS FAST')
                self.excluded_games[self.game_key]['throws'] = None
        else:
            self.excluded_games[self.game_key]['throws'] = None

    def set_values(self, key):
        if self.excluded_games[self.game_key].get(key) == '?':
            if ':' not in self.match_time or self.check_max_match_time(self.match_time, max_minute=13):
                key_data = self.info_dict.get(key, {})
                if isinstance(key_data, dict) and 'totals' in key_data:
                    totals = key_data['totals']
                    max_total = None
                    for item in totals:
                        try:
                            coefficient_under = float(item['coefficient_under'])
                            total_number = float(item['total_number'])

                            if coefficient_under > 1.64:
                                if max_total is None or total_number > max_total:
                                    max_total = total_number
                        except (ValueError, KeyError):
                            continue

                    if max_total is not None:
                        if key == 'yellow cards':
                            self.excluded_games[self.game_key][key] = math.floor(max_total + 1)
                        elif key == 'fouls':
                            self.excluded_games[self.game_key][key] = max_total
                        return True
            else:
                self.excluded_games[self.game_key][key] = None

    async def check_and_compare(self, key):
        if self.check_score():
            value = self.excluded_games[self.game_key].get(key)
            if isinstance(value, int):
                key_data = self.info_dict.get(key, {})
                if isinstance(key_data, dict) and 'totals' in key_data:
                    totals = key_data['totals']
                    min_total = None
                    for item in totals:
                        try:
                            coefficient_under = float(item['coefficient_under'])
                            total_number = float(item['total_number'])
                            if coefficient_under > 1.64:
                                if min_total is None or total_number < min_total:
                                    min_total = total_number
                        except (ValueError, KeyError):
                            continue

                    if min_total is not None:
                        if value < min_total:
                            await self._process_and_send_message(f'LIVE {key.upper()} RATE')
                            self.excluded_games[self.game_key][key] = None

    async def check_wide_throws(self):
        percentage = math.ceil(self.total_teams * 0.20)
        team1_rank = int(self.team1_info['rank'])
        team2_rank = int(self.team2_info['rank'])
        score1, score2 = map(int, self.match_score.split(':'))

        if team1_rank <= percentage and team2_rank >= self.total_teams - percentage:
            if score1 < score2:
                await self._process_and_send_message(text='NORMAL THROW-INS?')
                self.excluded_games[self.game_key]['throws'] = None
        elif team2_rank <= percentage and team1_rank >= self.total_teams - percentage:
            if score1 > score2:
                await self._process_and_send_message(text='NORMAL THROW-INS?')
                self.excluded_games[self.game_key]['throws'] = None
        elif team2_rank + 1 - team1_rank >= self.total_teams / 2:
            if self.check_max_match_time(self.match_time, max_minute=81) and score1 < score2:
                await self._process_and_send_message(text='DANGER1 THROW-INS?')
                self.excluded_games[self.game_key]['throws'] = None
        elif team1_rank + 1 - team2_rank >= self.total_teams / 2:
            if self.check_max_match_time(self.match_time, max_minute=81) and score1 > score2:
                await self._process_and_send_message(text='DANGER2 THROW-INS?')
                self.excluded_games[self.game_key]['throws'] = None
        else:
            self.excluded_games[self.game_key]['throws'] = None

    def check_quantity_games(self, quantity):
        if not self.team1_info or not self.team2_info:
            print(self.team1_name, self.team2_name)
            print(self.team_1_info, self.team2_info)
            raise QuantityError
        team1_games = int(self.team1_info['game_played'])
        team2_games = int(self.team2_info['game_played'])
        if not team1_games > quantity or not team2_games > quantity:
            self.excluded_games[self.game_key]['yellow cards'] = None
            self.excluded_games[self.game_key]['fouls'] = None
            self.excluded_games[self.game_key]['throws'] = None
            raise QuantityError

    def check_score(self):
        score1, score2 = map(int, self.info_dict['match_score'].split(':'))
        team1_rank = int(self.team1_info['rank'])
        team2_rank = int(self.team2_info['rank'])

        if team1_rank < team2_rank and score1 - score2 > 1:
            return True
        if team2_rank < team1_rank and score2 - score1 > 1:
            return True

    def is_best_rank_range(self):
        team1_rank = int(self.team1_info['rank'])
        team2_rank = int(self.team2_info['rank'])
        critical_ranks = list(range(1, 3)) + list(range(self.total_teams - 1, self.total_teams + 1))
        if team1_rank in critical_ranks and team2_rank in critical_ranks:
            return True

    async def _process_and_send_message(self, text):
        info = Info(
            live_data=self.info_dict,
            message=text
        )
        message = info.get_game_info()
        print(message)
        await self.telegram.send_message_with_files(message)

    def check_max_match_time(self, time: str, max_minute=75):
        if time and ':' in time:
            minutes = int(time.split(':')[0])
            if minutes < max_minute:
                return True

    def check_min_match_time(self, time, min_minute=45):
        if time and ':' in time:
            minutes = int(time.split(':')[0])
            if minutes > min_minute:
                return True


class SmartLiveCompare:
    def __init__(self, smart_data: dict, live_data: dict, league_data: dict, telegram: TelegramBot):
        self.smart_data = smart_data
        self.live_data = live_data
        self.league_data = league_data
        self.telegram = telegram
        self.files = [
            "graph/data/current_season_points.png",
            "graph/data/previous_season_points.png",
            "graph/data/current_season_stat.png",
            "graph/data/previous_season_stat.png",
            "graph/data/year_current_season_stat.png",
            "graph/data/year_previous_season_stat.png"
        ]

    async def compare(self):
        for statistic in self.live_data:
            if statistic in stats_dict.values():
                try:
                    smart_dct = self.smart_data['smart_data'][statistic]
                    total_under = smart_dct['ref_15_under_t']
                except KeyError as e:
                    print('self.smart_dataError', e)
                    continue
                if total_under:
                    await self.__search_total(statistic=statistic,
                                              statistic_key='totals',
                                              total_under=total_under,
                                              rate_direction='total')

    async def __search_total(self, statistic, statistic_key,
                             total_under, rate_direction):
        try:
            coeff_box = self.live_data[statistic][statistic_key]
        except KeyError:
            # print('SmartLiveCompare.search_total_coeff_box error: ', e)
            return

        for coeff_set in coeff_box:
            try:
                live_total = float(coeff_set['total_number'])
                coeff_under = float(coeff_set['coefficient_under'])

            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue

            if not isinstance(total_under, float):
                total_under = float(total_under)

            if live_total >= total_under and coeff_under > 1.65:
                await self.__send_message(rate_direction=rate_direction, statistic=statistic,
                                          live_total=live_total, coeff_under=coeff_under,
                                          total_under=total_under)

    async def __send_message(self, rate_direction, statistic, live_total, coeff_under, total_under):
        full_rate_direction = rate_direction + '_under'
        info = GameInfo(
            live_data=self.live_data,
            smart_data=self.smart_data,
            statistic_name=statistic,
            rate_direction=full_rate_direction,
            live_total=live_total,
            live_coeff=coeff_under,
            smart_total=total_under)
        self.__plot_graphs(statistic=statistic,
                           live_total=live_total,
                           rate_direction='TU')
        try:
            message = '\n'.join([info.get_game_info(), info.get_correction_key()])
        except TypeError:
            return
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
        current_viz.plot_team_stats(stat_key=statistic, season='current_season', sort_by='avg_individual_team')
        previous_viz.plot_team_stats(stat_key=statistic, season='previous_season', sort_by='avg_individual_team')
        matrix_viz = ScatterPlotBuilder(matrix_data=self.smart_data['smart_data']['year_matrix_data'])
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='year_current_season')
        matrix_viz.build_scatter_plot(stat_name=statistic,
                                      bookmaker_value=live_total,
                                      bet_direction=rate_direction,
                                      season='year_previous_season')
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

    def close_bet(self, key):
        parts = key.rstrip('➠').split('➠')
        try:
            self.smart_data['smart_data'][parts[1]][parts[2]] = None
        except KeyError as e:
            print('SmartLiveCompare.close_bet.ERROR: ', e)

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
