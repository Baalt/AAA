from line.analytics.structures import HomeDataStructure, AwayDataStructure
from line.analytics.line_utils.stat_math import StatMath


class ManualRefereeBets(StatMath):
    def __init__(self,
                 league,
                 big_data,
                 home_structure: HomeDataStructure,
                 away_structure: AwayDataStructure,
                 referee_data: dict,
                 statistic_name: str,
                 telegram):

        self.big_data = big_data
        self.home_structure = home_structure
        self.away_structure = away_structure
        self.referee_data = referee_data
        self.statistic_name = statistic_name
        self.telegram = telegram

    def calculate_percentages(self, seq, ref, idx):
        percentages = {}
        for offset in range(-2, 3):
            key = f"{offset:+d}" if offset > 0 else f"{offset:d}"  # Formatting key
            percentages[key] = self.calculate_percent_by_total(seq=seq, total=ref + offset)[idx]
        return percentages

    def search(self):
        data = {}
        try:
            ref_all_undert = self.search_under_total(seq=self.referee_data[self.statistic_name]['all'])
        except KeyError:
            ref_all_undert = None

        try:
            ref_15_undert = self.search_under_total(seq=self.referee_data[self.statistic_name]['first_15_elements'])
        except KeyError:
            ref_15_undert = None

        if ref_all_undert and ref_15_undert:
            ref_under = min(ref_all_undert, ref_15_undert)
            ref_all_under = self.calculate_percentages(seq=self.referee_data[self.statistic_name]['all'],
                                                       ref=ref_under, idx=0)
            ref_all_len = len(self.referee_data[self.statistic_name]['all'])
            ref_15_under = self.calculate_percentages(seq=self.referee_data[self.statistic_name]['first_15_elements'],
                                                      ref=ref_under, idx=0)
            ref_15_len = len(self.referee_data[self.statistic_name]['first_15_elements'])

            home_all_under = self.calculate_percentages(
                seq=self.home_structure.big_data_total_current_home_in_home_away_games,
                ref=ref_under, idx=0
            )
            home_all_len = len(self.home_structure.big_data_total_current_home_in_home_away_games)
            home_sim_high_under = self.calculate_percentages(
                seq=self.home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                ref=ref_under, idx=0
            )
            home_sim_high_len = len(
                self.home_structure.similar_command_total_current_home_big_data_home_away_games_high)
            home_sim_low_under = self.calculate_percentages(
                seq=self.home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                ref=ref_under, idx=0
            )
            home_sim_low_len = len(self.home_structure.similar_command_total_current_home_big_data_home_away_games_low)
            home_ly_under = self.calculate_percentages(
                seq=self.home_structure.last_year_total_current_home_command_in_home_away_games,
                ref=ref_under, idx=0
            )
            home_ly_len = len(self.home_structure.last_year_total_current_home_command_in_home_away_games)
            home_20_under = self.calculate_percentages(
                seq=self.home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            home_20_len = len(self.home_structure.last_20_games_total_current_home_by_year_in_home_away_games)
            home_12_under = self.calculate_percentages(
                seq=self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games,
                ref=ref_under, idx=0
            )
            home_12_len = len(self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games)
            home_8_under = self.calculate_percentages(
                seq=self.home_structure.last_8_games_total_current_home_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            home_8_len = len(self.home_structure.last_8_games_total_current_home_by_year_in_home_away_games)
            home_4_under = self.calculate_percentages(
                seq=self.home_structure.last_4_games_total_current_home_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            home_4_len = len(self.home_structure.last_4_games_total_current_home_by_year_in_home_away_games)

            away_all_under = self.calculate_percentages(
                seq=self.away_structure.big_data_total_current_away_in_home_away_games,
                ref=ref_under, idx=0
            )
            away_all_len = len(self.away_structure.big_data_total_current_away_in_home_away_games)
            away_sim_high_under = self.calculate_percentages(
                seq=self.away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                ref=ref_under, idx=0
            )
            away_sim_high_len = len(
                self.away_structure.similar_command_total_current_away_big_data_home_away_games_high)
            away_sim_low_under = self.calculate_percentages(
                seq=self.away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                ref=ref_under, idx=0
            )
            away_sim_low_len = len(self.away_structure.similar_command_total_current_away_big_data_home_away_games_low)
            away_ly_under = self.calculate_percentages(
                seq=self.away_structure.last_year_total_current_away_command_in_home_away_games,
                ref=ref_under, idx=0
            )
            away_ly_len = len(self.away_structure.last_year_total_current_away_command_in_home_away_games)
            away_20_under = self.calculate_percentages(
                seq=self.away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            away_20_len = len(self.away_structure.last_20_games_total_current_away_by_year_in_home_away_games)
            away_12_under = self.calculate_percentages(
                seq=self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games,
                ref=ref_under, idx=0
            )
            away_12_len = len(self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games)
            away_8_under = self.calculate_percentages(
                seq=self.away_structure.last_8_games_total_current_away_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            away_8_len = len(self.away_structure.last_8_games_total_current_away_by_year_in_home_away_games)
            away_4_under = self.calculate_percentages(
                seq=self.away_structure.last_4_games_total_current_away_by_year_in_home_away_games,
                ref=ref_under, idx=0
            )
            away_4_len = len(self.away_structure.last_4_games_total_current_away_by_year_in_home_away_games)

            data['ref_all_under'] = ref_all_under
            data['ref_all_len'] = ref_all_len
            data['ref_15_under'] = ref_15_under
            data['ref_15_len'] = ref_15_len
            data['home_all_under'] = home_all_under
            data['home_sim_high_under'] = home_sim_high_under
            data['home_sim_low_under'] = home_sim_low_under
            data['home_ly_under'] = home_ly_under
            data['home_20_under'] = home_20_under
            data['home_12_under'] = home_12_under
            data['home_8_under'] = home_8_under
            data['home_4_under'] = home_4_under
            data['away_all_under'] = away_all_under
            data['away_sim_high_under'] = away_sim_high_under
            data['away_sim_low_under'] = away_sim_low_under
            data['away_ly_under'] = away_ly_under
            data['away_20_under'] = away_20_under
            data['away_12_under'] = away_12_under
            data['away_8_under'] = away_8_under
            data['away_4_under'] = away_4_under
            data['home_all_len'] = home_all_len
            data['home_sim_high_len'] = home_sim_high_len
            data['home_sim_low_len'] = home_sim_low_len
            data['home_ly_len'] = home_ly_len
            data['home_20_len'] = home_20_len
            data['home_12_len'] = home_12_len
            data['home_8_len'] = home_8_len
            data['home_4_len'] = home_4_len
            data['away_all_len'] = away_all_len
            data['away_sim_high_len'] = away_sim_high_len
            data['away_sim_low_len'] = away_sim_low_len
            data['away_ly_len'] = away_ly_len
            data['away_20_len'] = away_20_len
            data['away_12_len'] = away_12_len
            data['away_8_len'] = away_8_len
            data['away_4_len'] = away_4_len

        try:
            ref_all_over = self.search_over_total(seq=self.referee_data[self.statistic_name]['all'])
        except KeyError:
            ref_all_over = None

        try:
            ref_15_over = self.search_over_total(seq=self.referee_data[self.statistic_name]['first_15_elements'])
        except KeyError:
            ref_15_over = None

        if ref_all_over and ref_15_over:
            ref_over = max(ref_all_over, ref_15_over)

            ref_all_over = self.calculate_percentages(seq=self.referee_data[self.statistic_name]['all'],
                                                      ref=ref_over, idx=1)
            ref_15_over = self.calculate_percentages(seq=self.referee_data[self.statistic_name]['first_15_elements'],
                                                     ref=ref_over, idx=1)

            home_all_over = self.calculate_percentages(
                seq=self.home_structure.big_data_total_current_home_in_home_away_games,
                ref=ref_over, idx=1
            )
            home_sim_high_over = self.calculate_percentages(
                seq=self.home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                ref=ref_over, idx=1
            )
            home_sim_low_over = self.calculate_percentages(
                seq=self.home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                ref=ref_over, idx=1
            )
            home_ly_over = self.calculate_percentages(
                seq=self.home_structure.last_year_total_current_home_command_in_home_away_games,
                ref=ref_over, idx=1
            )
            home_20_over = self.calculate_percentages(
                seq=self.home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )
            home_12_over = self.calculate_percentages(
                seq=self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games,
                ref=ref_over, idx=1
            )
            home_8_over = self.calculate_percentages(
                seq=self.home_structure.last_8_games_total_current_home_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )
            home_4_over = self.calculate_percentages(
                seq=self.home_structure.last_4_games_total_current_home_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )

            away_all_over = self.calculate_percentages(
                seq=self.away_structure.big_data_total_current_away_in_home_away_games,
                ref=ref_over, idx=1
            )
            away_sim_high_over = self.calculate_percentages(
                seq=self.away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                ref=ref_over, idx=1
            )
            away_sim_low_over = self.calculate_percentages(
                seq=self.away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                ref=ref_over, idx=1
            )
            away_ly_over = self.calculate_percentages(
                seq=self.away_structure.last_year_total_current_away_command_in_home_away_games,
                ref=ref_over, idx=1
            )
            away_20_over = self.calculate_percentages(
                seq=self.away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )
            away_12_over = self.calculate_percentages(
                seq=self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games,
                ref=ref_over, idx=1
            )
            away_8_over = self.calculate_percentages(
                seq=self.away_structure.last_8_games_total_current_away_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )
            away_4_over = self.calculate_percentages(
                seq=self.away_structure.last_4_games_total_current_away_by_year_in_home_away_games,
                ref=ref_over, idx=1
            )
            data['ref_all_over'] = ref_all_over
            data['ref_15_over'] = ref_15_over
            data['home_all_over'] = home_all_over
            data['home_sim_high_over'] = home_sim_high_over
            data['home_sim_low_over'] = home_sim_low_over
            data['home_ly_over'] = home_ly_over
            data['home_20_over'] = home_20_over
            data['home_12_over'] = home_12_over
            data['home_8_over'] = home_8_over
            data['home_4_over'] = home_4_over
            data['away_all_over'] = away_all_over
            data['away_sim_high_over'] = away_sim_high_over
            data['away_sim_low_over'] = away_sim_low_over
            data['away_ly_over'] = away_ly_over
            data['away_20_over'] = away_20_over
            data['away_12_over'] = away_12_over
            data['away_8_over'] = away_8_over
            data['away_4_over'] = away_4_over

        return data



