import os
import time

from graph.matrix_stats_viz import ScatterPlotBuilder
from live.analytics.game_info import GameInfo, Info
from telega.telegram_bot import TelegramBot
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from utils.stat_switcher import stats_dict

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


class MatchAnalyzer:
    def __init__(self, info_dict, excluded_games, game_key, tel):
        self.info_dict = info_dict
        self.league = info_dict['league']
        self.match_score = info_dict['match_score']
        self.match_time = info_dict['match_time']
        self.team1_name = info_dict['team1_name']
        self.team2_name = info_dict['team2_name']
        self.total_teams = info_dict['total_teams']
        self.tournament_info = info_dict['tournament_info']
        self.team1_info = None
        self.team2_info = None
        self.excluded_games = excluded_games
        self.game_key = game_key
        self.telegram = tel
        self.__assign_teams()

    def __assign_teams(self):
        for team_info in self.tournament_info:
            if team_info['name'] == self.team1_name:
                self.team1_info = team_info
            elif team_info['name'] == self.team2_name:
                self.team2_info = team_info

    async def check_conditions(self):
        if not self.team1_info or not self.team2_info:
            return False

        percentage = self.total_teams * 0.15

        team1_rank = int(self.team1_info['rank'])
        team2_rank = int(self.team2_info['rank'])

        score1, score2 = map(int, self.match_score.split(':'))

        if team1_rank <= percentage and team2_rank >= self.total_teams - percentage:
            if score1 < score2 and self.check_match_time(self.match_time):
                await self._process_and_send_message()
                self.excluded_games[self.game_key]['check'] = None
            elif self.match_time == '45:00' and score1 == score2:
                await self._process_and_send_message()
                self.excluded_games[self.game_key]['check'] = None
        elif (team2_rank - team1_rank) >= self.total_teams / 2:
            if self.match_time == '45:00' and score1 < score2:
                await self._process_and_send_message()
                self.excluded_games[self.game_key]['check'] = None

    def check_match_time(self, match_time: str, max_minute=65):
        if match_time and ':' in match_time:
            minutes = int(match_time.split(':')[0])
            if minutes < max_minute:
                return True
        return None

    async def _process_and_send_message(self):
        info = Info(
            live_data=self.info_dict,
        )
        message = info.get_game_info()
        print(message)
        await self.telegram.send_message_with_files(message)


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
