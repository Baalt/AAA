import os
import time

from graph.teams_stats_viz import TeamsStatsVisualizer
from graph.matrix_stats_viz import ScatterPlotBuilder
from line.analytics.message_builder import KushMessageBuilder, ExpressMessageBuilder, RefereeMessageBuilder
from line.analytics.structures import HomeDataStructure, AwayDataStructure
from utils.stat_switcher import stats_dict


class Catcher:
    def __init__(self,
                 telegram,
                 home_structure: HomeDataStructure,
                 away_structure: AwayDataStructure,
                 big_match_data: dict,
                 coefficients: dict,
                 statistic_name: str,
                 all_league_data: dict,
                 referee_data: dict,
                 big_matrix_data,
                 year_matrix_data):

        self.telegram = telegram
        self.home_structure = home_structure
        self.away_structure = away_structure
        self.big_match_data = big_match_data
        self.coefficients = coefficients
        self.big_matrix_data = big_matrix_data
        self.year_matrix_data = year_matrix_data

        self.all_league_data = all_league_data
        self.referee_data = referee_data
        self.files = [
            "graph/data/current_season_points.png",
            "graph/data/previous_season_points.png",
            "graph/data/year_current_season_stat.png",
            "graph/data/year_previous_season_stat.png",
            "graph/data/current_season_stat.png",
            "graph/data/previous_season_stat.png"
        ]

        if statistic_name in stats_dict.keys():
            self.statistic_name = stats_dict[statistic_name]
        else:
            self.statistic_name = statistic_name

    def calculate_percentage(self, coeff_set, seq, double=None):
        try:
            total = float(coeff_set['total_number'])
            if double:
                total *= 2
        except ValueError:
            print("Invalid total value. Conversion to float failed.")
            return None, None
        if not seq:
            return None, None

        less_than_total = 0
        greater_than_total = 0

        for number in seq:
            if number < total:
                less_than_total += 1
            elif number > total:
                greater_than_total += 1

        total_count = len(seq)
        less_than_percentage = round((less_than_total / total_count) * 100, 2)
        greater_than_percentage = round((greater_than_total / total_count) * 100, 2)

        return less_than_percentage, greater_than_percentage

    def handicap_percentage_calculate(self, coeff_set: dict, current_seq: list, opposing_seq: list):
        try:
            coeff_total = float(coeff_set['total_number'])
        except ValueError:
            print("Invalid total value. Conversion to float failed.")
            return

        if not current_seq:
            print("Length of current_seq is zero.")
            return

        if len(current_seq) != len(opposing_seq):
            print("Length of current_seq is not equal to the length of opposing_seq.")
            return

        count_current_seq_greater = 0
        count_current_seq_less = 0

        idx = 0
        for total in current_seq:
            total_plus_handicap = (total + coeff_total) - opposing_seq[idx]
            idx += 1

            if total_plus_handicap > 0:
                count_current_seq_greater += 1
            elif total_plus_handicap < 0:
                count_current_seq_less += 1

        total_count = len(current_seq)
        percent_current_seq_greater = round((count_current_seq_greater / total_count) * 100, 2)
        return percent_current_seq_greater

    def referee_calculate(self, statistic_name, coeff_set, double=None):
        try:
            if self.referee_data:
                under_all, over_all = self.calculate_percentage(
                    coeff_set=coeff_set,
                    seq=self.referee_data[statistic_name]['all'],
                    double=double)
                under_15, over_15 = self.calculate_percentage(
                    coeff_set=coeff_set,
                    seq=self.referee_data[statistic_name]['first_15_elements'],
                    double=double)
                return under_all, over_all, under_15, over_15
        except KeyError:
            return None

    async def search_kush_rate(self, statistic_name: str, league_name: str, coefficients: dict, coeff_set: dict,
                               rate_direction: str, coeff_under_over_key: str, big_data_current_percent: float,
                               big_data_opposing_percent: float, last_year_current_percent: float,
                               last_year_opposing_percent: float, similar_current_percent_low: float,
                               similar_opposing_percent_low: float, similar_current_percent_high: float,
                               similar_opposing_percent_high: float, last_20_current_percent: float,
                               last_20_opposing_percent: float, last_12_current_percent: float,
                               last_12_opposing_percent: float, last_8_current_percent: float,
                               last_8_opposing_percent: float, last_4_current_percent: float,
                               last_4_opposing_percent: float, referee_all=None, referee_15=None):
        self.bet_direction = rate_direction
        self.coeff_set = coeff_set
        self.coeff_total = float(self.coeff_set['total_number'])
        try:
            last_20_percent = (last_20_current_percent + last_20_opposing_percent) / 2
            last_12_percent = (last_12_current_percent + last_12_opposing_percent) / 2
            last_8_percent = (last_8_current_percent + last_8_opposing_percent) / 2
            last_4_percent = (last_4_current_percent + last_4_opposing_percent) / 2
        except TypeError:
            return
        try:
            similar_percent_low = (similar_current_percent_low + similar_opposing_percent_low) / 2
        except TypeError:
            similar_percent_low = None
        try:
            similar_percent_high = (similar_current_percent_high + similar_opposing_percent_high) / 2
        except TypeError:
            similar_percent_high = None
        try:
            big_data_percent = (big_data_current_percent + big_data_opposing_percent) / 2
        except TypeError:
            big_data_percent = None
        try:
            last_year_percent = (last_year_current_percent + last_year_opposing_percent) / 2
        except TypeError:
            last_year_percent = None

        high_percent_1, low_percent = 86, 66.6

        if statistic_name == 'ЖК' or statistic_name == 'Фолы':
            if referee_15 and self.referee_data[statistic_name]['count'] > 9 and (
                    rate_direction == 'TU' or rate_direction == 'TO'):
                is_high_percent = referee_15 > high_percent_1
                is_fouls_stat = statistic_name == 'Фолы'
                is_total_under = rate_direction == 'Total_Under'
                is_total_over = rate_direction == 'Total_Over'
                is_coeff_above_avg = self.coeff_total > self.referee_data[statistic_name]['avg'] + 7
                is_coeff_below_avg = self.coeff_total < self.referee_data[statistic_name]['avg'] - 7
                if is_high_percent or (is_fouls_stat and is_total_under and is_coeff_above_avg) or (
                        is_fouls_stat and is_total_over and is_coeff_below_avg):
                    await self.process_high_percent_message(
                        statistic_name=statistic_name,
                        league_name=league_name,
                        coefficients=coefficients,
                        coeff_set=coeff_set,
                        rate_direction=rate_direction,
                        coeff_under_over_key=coeff_under_over_key,
                        big_data_percent=big_data_percent,
                        last_year_percent=last_year_percent,
                        similar_percent_low=similar_percent_low,
                        similar_percent_high=similar_percent_high,
                        last_20_percent=last_20_percent,
                        last_12_percent=last_12_percent,
                        last_8_percent=last_8_percent,
                        last_4_percent=last_4_percent,
                        referee_all=referee_all,
                        referee_15=referee_15,
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

        percent_1 = min(last_20_percent, last_12_percent, last_8_percent, last_4_percent)
        if percent_1 >= 90:
            await self.process_high_percent_message(statistic_name=statistic_name,
                                                    league_name=league_name,
                                                    coefficients=coefficients,
                                                    coeff_set=coeff_set,
                                                    rate_direction=rate_direction,
                                                    coeff_under_over_key=coeff_under_over_key,
                                                    big_data_percent=big_data_percent,
                                                    last_year_percent=last_year_percent,
                                                    similar_percent_low=similar_percent_low,
                                                    similar_percent_high=similar_percent_high,
                                                    last_20_percent=last_20_percent,
                                                    last_12_percent=last_12_percent,
                                                    last_8_percent=last_8_percent,
                                                    last_4_percent=last_4_percent,
                                                    referee_all=referee_all,
                                                    referee_15=referee_15,
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

        last_20_kush_by_rate = self.kush_calculate(last_20_percent, coeff_set[coeff_under_over_key])
        last_12_kush_by_rate = self.kush_calculate(last_12_percent, coeff_set[coeff_under_over_key])
        last_8_kush_by_rate = self.kush_calculate(last_8_percent, coeff_set[coeff_under_over_key])
        last_4_kush_by_rate = self.kush_calculate(last_4_percent, coeff_set[coeff_under_over_key])

        min_kush = min(last_20_kush_by_rate, last_12_kush_by_rate, last_8_kush_by_rate, last_4_kush_by_rate)
        if percent_1 > low_percent and min_kush >= 0.3:
            big_data_kush_by_rate = self.kush_calculate(big_data_percent, coeff_set[coeff_under_over_key])
            last_year_kush_by_rate = self.kush_calculate(last_year_percent, coeff_set[coeff_under_over_key])
            similar_kush_by_rate_low = self.kush_calculate(similar_percent_low, coeff_set[coeff_under_over_key])
            similar_kush_by_rate_high = self.kush_calculate(similar_percent_high, coeff_set[coeff_under_over_key])

            await self.process_kush_message(
                statistic_name=statistic_name,
                league_name=league_name,
                coefficients=coefficients,
                coeff_set=coeff_set,
                rate_direction=rate_direction,
                coeff_under_over_key=coeff_under_over_key,
                big_data_percent=big_data_percent,
                last_year_percent=last_year_percent,
                similar_percent_low=similar_percent_low,
                similar_percent_high=similar_percent_high,
                last_20_percent=last_20_percent,
                last_12_percent=last_12_percent,
                last_8_percent=last_8_percent,
                last_4_percent=last_4_percent,
                referee_all=referee_all,
                referee_15=referee_15,
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
                last_4_opposing_percent=last_4_opposing_percent,
                big_data_kush_by_rate=big_data_kush_by_rate,
                last_year_kush_by_rate=last_year_kush_by_rate,
                similar_kush_by_rate_low=similar_kush_by_rate_low,
                similar_kush_by_rate_high=similar_kush_by_rate_high,
                last_20_kush_by_rate=last_20_kush_by_rate,
                last_12_kush_by_rate=last_12_kush_by_rate,
                last_8_kush_by_rate=last_8_kush_by_rate,
                last_4_kush_by_rate=last_4_kush_by_rate)

    async def process_high_percent_message(self, statistic_name, league_name, coefficients, coeff_set,
                                           rate_direction, coeff_under_over_key, big_data_percent,
                                           last_year_percent, similar_percent_low, similar_percent_high,
                                           last_20_percent, last_12_percent, last_8_percent,
                                           last_4_percent, referee_all, referee_15,
                                           big_data_current_percent, big_data_opposing_percent,
                                           last_year_current_percent, last_year_opposing_percent,
                                           similar_current_percent_low, similar_opposing_percent_low,
                                           similar_current_percent_high, similar_opposing_percent_high,
                                           last_20_current_percent, last_20_opposing_percent,
                                           last_12_current_percent, last_12_opposing_percent,
                                           last_8_current_percent, last_8_opposing_percent,
                                           last_4_current_percent, last_4_opposing_percent):
        coefficient = coeff_set[coeff_under_over_key]
        if not isinstance(coefficient, float):
            coefficient = float(coefficient)
        if coefficient > 1.1:
            exp_message = ExpressMessageBuilder(
                statistic_name=statistic_name,
                league_name=league_name,
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
                category='express 90+',
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
            message = exp_message.get_message()
            if referee_15:
                referee_message = RefereeMessageBuilder(
                    referee_name=self.referee_data['referee_name'],
                    all_data=referee_all,
                    last15=referee_15,
                    average=self.referee_data[statistic_name]['avg'],
                    length=self.referee_data[statistic_name]['count'],
                    coeff_total=coeff_set['total_number'],
                    rate_direction=rate_direction)
                message = '\n'.join([message, referee_message.get_message()])
            print(message)
            self.__plot_graphs()
            await self.telegram.send_message_with_files(message, *self.files)

    async def process_kush_message(self, statistic_name: str, league_name: str, coeff_set,
                                   coeff_under_over_key, coefficients: dict, rate_direction: str,
                                   big_data_percent: float, last_year_percent: float,
                                   similar_percent_low: float, similar_percent_high: float,
                                   last_20_percent: float, last_12_percent: float,
                                   last_8_percent: float, last_4_percent: float,
                                   big_data_kush_by_rate: float, last_year_kush_by_rate,
                                   similar_kush_by_rate_low: float, similar_kush_by_rate_high: float,
                                   last_20_kush_by_rate: float, last_12_kush_by_rate: float,
                                   last_8_kush_by_rate: float, last_4_kush_by_rate: float,
                                   big_data_current_percent: float, big_data_opposing_percent: float,
                                   last_year_current_percent: float, last_year_opposing_percent: float,
                                   similar_current_percent_low: float, similar_opposing_percent_low: float,
                                   similar_current_percent_high: float, similar_opposing_percent_high: float,
                                   last_20_current_percent: float, last_20_opposing_percent: float,
                                   last_12_current_percent: float, last_12_opposing_percent: float,
                                   last_8_current_percent: float, last_8_opposing_percent: float,
                                   last_4_current_percent: float, last_4_opposing_percent: float,
                                   referee_all, referee_15):

        kush_message = KushMessageBuilder(
            statistic_name=statistic_name,
            league_name=league_name,
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
            last_4_opposing_percent=last_4_opposing_percent
        )

        message = kush_message.get_message()
        if referee_15:
            referee_message = RefereeMessageBuilder(
                referee_name=self.referee_data['referee_name'],
                all_data=referee_all,
                last15=referee_15,
                average=self.referee_data[statistic_name]['avg'],
                length=self.referee_data[statistic_name]['count'],
                coeff_total=coeff_set['total_number'],
                rate_direction=rate_direction)
            message = '\n'.join([message, referee_message.get_message()])
        print(message)
        self.__plot_graphs()
        await self.telegram.send_message_with_files(message, *self.files)

    def kush_calculate(self, percent, coefficient):
        if not isinstance(percent, float):
            percent = float(percent)
        if not isinstance(coefficient, float):
            coefficient = float(coefficient)
        kush = ((percent * (coefficient - 1)) - (100 - percent)) / 100
        return kush

    def __plot_graphs(self):
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
        matrix_viz = ScatterPlotBuilder(matrix_data=self.year_matrix_data)
        matrix_viz.build_scatter_plot(stat_name=self.statistic_name,
                                      bookmaker_value=self.coeff_total,
                                      bet_direction=self.bet_direction,
                                      season='year_current_season')
        matrix_viz.build_scatter_plot(stat_name=self.statistic_name,
                                      bookmaker_value=self.coeff_total,
                                      bet_direction=self.bet_direction,
                                      season='year_previous_season')
        matrix_viz = ScatterPlotBuilder(matrix_data=self.big_matrix_data)
        matrix_viz.build_scatter_plot(stat_name=self.statistic_name,
                                      bookmaker_value=self.coeff_total,
                                      bet_direction=self.bet_direction,
                                      season='current_season')
        matrix_viz.build_scatter_plot(stat_name=self.statistic_name,
                                      bookmaker_value=self.coeff_total,
                                      bet_direction=self.bet_direction,
                                      season='previous_season')
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
