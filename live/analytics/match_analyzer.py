import os
import time

from graph.matrix_stats_viz import ScatterPlotBuilder
from live.analytics.game_info import GameInfo, ScoreInfo, RedYellowCardInfo
from telega.telegram_bot import TelegramBot
from utils.pickle_manager import PickleHandler
from utils.func import get_today_date
from utils.stat_switcher import stats_dict

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


class ScoreCompare:
    def __init__(self, live_data: dict, telegram: TelegramBot, excluded_games: dict, game_key: str):
        self.live_data = live_data
        self.excluded_games = excluded_games
        self.game_key = game_key
        self.telegram = telegram

    async def compare(self):
        try:
            if ':' in self.live_data['match_score']:
                parts = self.live_data['match_score'].split(':')
                score1 = int(parts[0].strip())
                score2 = int(parts[1].strip())
                if (score1 - score2) > 3.5 or (score2 - score1) > 3.5:
                    info = ScoreInfo(live_data=self.live_data)
                    message = info.get_game_info()
                    print(message)
                    await self.telegram.send_message_with_files(message)
                    self.excluded_games[self.game_key]['score_under'] = None
        except KeyError as e:
            print('ScoreCompare.compare.ERROR:', e)

class RedLiveCompare:
    def __init__(self, live_data: dict, telegram: TelegramBot, excluded_games: dict, game_key: str):
        self.live_data = live_data
        self.telegram = telegram
        self.excluded_games = excluded_games
        self.game_key = game_key
        self.is_fouls = 'fouls' in self.live_data

    async def compare(self):
        try:
            if self.live_data['match_time'] == '45:00' and self.is_fouls:
                print(self.game_key, 'match_time == 45:00')
                if ':' in self.live_data['red_score'] and self.live_data['red_score'] != '0 : 0':
                    await self._process_and_send_message()
                if self.live_data['match_stats']['Yellow cards']:
                    yellow_1 = int(self.live_data['match_stats']['Yellow cards']['team1'])
                    yellow_2 = int(self.live_data['match_stats']['Yellow cards']['team2'])
                    if (yellow_1 + yellow_2) > 3.5:
                        await self._process_and_send_message()

                self.excluded_games[self.game_key]['red_yellow'] = None
        except KeyError as e:
            print('RedLiveCompare.compare.ERROR:', e)

    async def _process_and_send_message(self):
        """
        Processes the live data to extract necessary information and sends a message via Telegram.
        """
        live_list = [float(data['total_number']) for data in self.live_data['fouls']['totals']]
        fouls = max(live_list) if live_list else None
        info = RedYellowCardInfo(
            live_data=self.live_data,
            yellow_cards=self.live_data['yellow_score'],
            fouls=fouls
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
            if live_total >= total_under and coeff_under > 1.3:
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
