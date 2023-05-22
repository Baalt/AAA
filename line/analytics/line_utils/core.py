import os
import time

from graph.teams_stats_viz import TeamsStatsVisualizer
from line.analytics.message_builder import RateMessageBuilder, ExpressMessageBuilder
from line.analytics.structures import HomeDataStructure, AwayDataStructure
from utils.stat_switcher import stats_dict
from utils.error import HandicapNotMatchSeqError


class Catcher:
    def __init__(self,
                 telegram,
                 home_structure: HomeDataStructure,
                 away_structure: AwayDataStructure,
                 big_match_data: dict,
                 coefficients: dict,
                 statistic_name: str,
                 all_league_data: dict):

        self.telegram = telegram
        self.home_structure = home_structure
        self.away_structure = away_structure
        self.big_match_data = big_match_data
        self.coefficients = coefficients

        self.all_league_data = all_league_data
        self.files = [
            "graph/data/current_season_points.png",
            "graph/data/previous_season_points.png",
            "graph/data/current_season_stat.png",
            "graph/data/previous_season_stat.png"
        ]

        if statistic_name in stats_dict.keys():
            self.statistic_name = stats_dict[statistic_name]
        else:
            self.statistic_name = statistic_name

    def total_calculation(self, coeff_set, seq: list):
        over_list = []
        under_list = []
        try:
            coeff_total = float(coeff_set['total_number'])
            for total in seq:
                if total > coeff_total:
                    over_list.append(total)
                elif total < coeff_total:
                    under_list.append(total)

            count_under = len(under_list)
            count_over = len(over_list)
            try:
                under_percent = (count_under * 100) / (count_over + count_under)
            except ZeroDivisionError:
                under_percent = None

            try:
                over_percent = (count_over * 100) / (count_over + count_under)
            except ZeroDivisionError:
                over_percent = None

            return under_percent, over_percent

        except Exception as err:
            raise err
        #     print('Catcher.total_calculation Error: ', err)
        #     return None

    def handicap_calculation(self, coeff_set: dict, current_seq: list, opposing_seq: list):
        if len(current_seq) == len(opposing_seq):
            win_list = []
            lose_list = []
            try:
                coeff_total = float(coeff_set['total_number'])
                idx = 0
                for total in current_seq:
                    total_plus_handicap = (total + coeff_total) - opposing_seq[idx]
                    idx += 1

                    if total_plus_handicap > 0:
                        win_list.append(total)
                    elif total_plus_handicap < 0:
                        lose_list.append(total)

                count_win = len(win_list)
                count_lose = len(lose_list)

                denominator = count_win + count_lose
                if denominator:
                    win_percent = (count_win * 100) / denominator
                    return win_percent

                raise ZeroDivisionError

            except Exception as err:
                print('rate_search Error: ', err)
                raise err

        raise HandicapNotMatchSeqError(
            f'Do not match current and opposing seqs {len(current_seq)} - {len(opposing_seq)}')

    async def search_kush_rate(self,
                               statistic_name: str,
                               league_name: str,
                               coefficients: dict,
                               coeff_set: dict,
                               rate_direction: str,
                               coeff_under_over_key: str,
                               big_data_current_percent: float,
                               big_data_opposing_percent: float,
                               last_year_current_percent: float,
                               last_year_opposing_percent: float,
                               similar_current_percent_low: float,
                               similar_opposing_percent_low: float,
                               similar_current_percent_high: float,
                               similar_opposing_percent_high: float,
                               last_20_current_percent: float,
                               last_20_opposing_percent: float,
                               last_12_current_percent: float,
                               last_12_opposing_percent: float,
                               last_8_current_percent: float,
                               last_8_opposing_percent: float,
                               last_4_current_percent: float,
                               last_4_opposing_percent: float):
        self.league_name = league_name
        try:
            last_20_percent = (last_20_current_percent + last_20_opposing_percent) / 2
            last_12_percent = (last_12_current_percent + last_12_opposing_percent) / 2
            last_8_percent = (last_8_current_percent + last_8_opposing_percent) / 2
            last_4_percent = (last_4_current_percent + last_4_opposing_percent) / 2
            similar_percent_low = (similar_current_percent_low + similar_opposing_percent_low) / 2
            similar_percent_high = (similar_current_percent_high + similar_opposing_percent_high) / 2
            big_data_percent = (big_data_current_percent + big_data_opposing_percent) / 2
            last_year_percent = (last_year_current_percent + last_year_opposing_percent) / 2
        except TypeError:
            return
        high_percent_1, high_percent_2, average_percent = 90, 85, 66.6
        percent_1 = min(last_12_percent, last_8_percent, last_4_percent)
        percent_2 = min(similar_percent_low, similar_percent_high, last_20_percent)
        if percent_1 >= high_percent_1 and percent_2 >= high_percent_2:
            coefficient = coeff_set[coeff_under_over_key]
            if not isinstance(coefficient, float):
                coefficient = float(coefficient)
            if coefficient > 1.27:
                message = ExpressMessageBuilder(statistic_name=statistic_name,
                                                league_name=self.league_name,
                                                big_data_percent=big_data_percent,
                                                last_year_percent=last_year_percent,
                                                similar_percent_low=similar_percent_low,
                                                similar_percent_high=similar_percent_high,
                                                last_20_percent=last_20_percent,
                                                last_12_percent=last_12_percent,
                                                last_8_percent=last_8_percent,
                                                last_4_percent=last_4_percent,
                                                big_match_data=self.big_match_data,
                                                coefficients=coefficients,
                                                coeff_total=coeff_set['total_number'],
                                                coeff_value=coeff_set[coeff_under_over_key],
                                                rate_direction=rate_direction,
                                                category='Kush+',
                                                big_data_current_percent=big_data_current_percent,
                                                big_data_opposing_percent=big_data_opposing_percent,
                                                last_year_current_percent=last_year_current_percent,
                                                last_year_opposing_percent=last_year_opposing_percent,
                                                similar_current_percent_low=similar_current_percent_low,
                                                similar_opposing_percent_low=similar_opposing_percent_low,
                                                similar_current_percent_high=similar_current_percent_high,
                                                similar_opposing_percent_high=similar_opposing_percent_high,
                                                last_20_current_percent=last_20_current_percent,
                                                last_20_opposing_percent=last_20_opposing_percent,
                                                last_12_current_percent=last_12_current_percent,
                                                last_12_opposing_percent=last_12_opposing_percent,
                                                last_8_current_percent=last_8_current_percent,
                                                last_8_opposing_percent=last_8_opposing_percent,
                                                last_4_current_percent=last_4_current_percent,
                                                last_4_opposing_percent=last_4_opposing_percent)
                print(message.get_express_rate_message())
                self.__plot_graphs(statistic=self.statistic_name)
                await self.telegram.send_message_with_files(message.get_express_rate_message(), *self.files)

        big_data_kush_by_rate = self.kush_calculate(percent=big_data_percent,
                                                    coefficient=coeff_set[coeff_under_over_key])
        last_year_kush_by_rate = self.kush_calculate(percent=last_year_percent,
                                                     coefficient=coeff_set[coeff_under_over_key])
        similar_kush_by_rate_low = self.kush_calculate(percent=similar_percent_low,
                                                       coefficient=coeff_set[coeff_under_over_key])
        similar_kush_by_rate_high = self.kush_calculate(percent=similar_percent_high,
                                                        coefficient=coeff_set[coeff_under_over_key])
        last_20_kush_by_rate = self.kush_calculate(percent=last_20_percent,
                                                   coefficient=coeff_set[coeff_under_over_key])
        last_12_kush_by_rate = self.kush_calculate(percent=last_12_percent,
                                                   coefficient=coeff_set[coeff_under_over_key])
        last_8_kush_by_rate = self.kush_calculate(percent=last_8_percent,
                                                  coefficient=coeff_set[coeff_under_over_key])
        last_4_kush_by_rate = self.kush_calculate(percent=last_4_percent,
                                                  coefficient=coeff_set[coeff_under_over_key])
        try:
            min_kush = min(similar_kush_by_rate_low, similar_kush_by_rate_high,
                           last_20_kush_by_rate, last_12_kush_by_rate, last_8_kush_by_rate, last_4_kush_by_rate)
        except TypeError:
            return

        if percent_1 > average_percent and percent_2 > average_percent and min_kush >= 0.3:
            message = RateMessageBuilder(statistic_name=statistic_name,
                                         league_name=self.league_name,
                                         big_data_percent=big_data_percent,
                                         last_year_percent=last_year_percent,
                                         similar_percent_low=similar_percent_low,
                                         similar_percent_high=similar_percent_high,
                                         last_20_percent=last_20_percent,
                                         last_12_percent=last_12_percent,
                                         last_8_percent=last_8_percent,
                                         last_4_percent=last_4_percent,
                                         big_match_data=self.big_match_data,
                                         coefficients=coefficients,
                                         coeff_total=coeff_set['total_number'],
                                         coeff_value=coeff_set[coeff_under_over_key],
                                         rate_direction=rate_direction,
                                         category='Kush+',
                                         big_data_kush_by_rate=big_data_kush_by_rate,
                                         last_year_kush_by_rate=last_year_kush_by_rate,
                                         similar_kush_by_rate_low=similar_kush_by_rate_low,
                                         similar_kush_by_rate_high=similar_kush_by_rate_high,
                                         last_20_kush_by_rate=last_20_kush_by_rate,
                                         last_12_kush_by_rate=last_12_kush_by_rate,
                                         last_8_kush_by_rate=last_8_kush_by_rate,
                                         last_4_kush_by_rate=last_4_kush_by_rate,
                                         big_data_current_percent=big_data_current_percent,
                                         big_data_opposing_percent=big_data_opposing_percent,
                                         last_year_current_percent=last_year_current_percent,
                                         last_year_opposing_percent=last_year_opposing_percent,
                                         similar_current_percent_low=similar_current_percent_low,
                                         similar_opposing_percent_low=similar_opposing_percent_low,
                                         similar_current_percent_high=similar_current_percent_high,
                                         similar_opposing_percent_high=similar_opposing_percent_high,
                                         last_20_current_percent=last_20_current_percent,
                                         last_20_opposing_percent=last_20_opposing_percent,
                                         last_12_current_percent=last_12_current_percent,
                                         last_12_opposing_percent=last_12_opposing_percent,
                                         last_8_current_percent=last_8_current_percent,
                                         last_8_opposing_percent=last_8_opposing_percent,
                                         last_4_current_percent=last_4_current_percent,
                                         last_4_opposing_percent=last_4_opposing_percent)
            print(message.get_kush_rate_message())
            self.__plot_graphs(statistic=self.statistic_name)
            await self.telegram.send_message_with_files(message.get_kush_rate_message(), *self.files)

    def kush_calculate(self, percent, coefficient):
        if not isinstance(percent, float):
            percent = float(percent)
        if not isinstance(coefficient, float):
            coefficient = float(coefficient)
        if percent > 0 and percent <= 100:
            kush = ((percent * (coefficient - 1)) - (100 - percent)) / 100
            return kush
        return None

    def __plot_graphs(self, statistic):
        self.delete_files_in_folder(folder_path='graph/data')
        current_viz = TeamsStatsVisualizer(
            data=self.all_league_data['current_season'],
            team_name_1=self.big_match_data['home_command_name'],
            team_name_2=self.big_match_data['away_command_name'])
        current_viz.plot_points(
            data_lst=self.all_league_data['current_season']['goals'],
            season='current_season')
        previous_viz = TeamsStatsVisualizer(
            data=self.all_league_data['previous_season'],
            team_name_1=self.big_match_data['home_command_name'],
            team_name_2=self.big_match_data['away_command_name'])
        previous_viz.plot_points(
            data_lst=self.all_league_data['previous_season']['goals'],
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
