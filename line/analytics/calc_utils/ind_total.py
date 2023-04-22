from line.analytics.calc_utils.core import BoundaryLiveValues


class LiveIndividualCalculation(BoundaryLiveValues):
    def calculate_individual_1_live_data(self, home_structure, away_structure, percent):
        big_data_current_result = self.total_calculation(
            seq=home_structure.big_data_individual_total_current_home_in_home_away_games,
            percent=percent)
        big_data_opposing_result = self.total_calculation(
            seq=away_structure.big_data_individual_total_opposing_teams_current_away_in_home_away_games,
            percent=percent)
        last_year_current_result = self.total_calculation(
            seq=home_structure.last_year_individual_total_current_home_command_in_home_away_games,
            percent=percent)
        last_year_opposing_result = self.total_calculation(
            seq=away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games,
            percent=percent)
        high_similar_current_result = self.total_calculation(
            seq=home_structure.similar_command_individual_total_current_home_command_in_home_away_games_high,
            percent=percent)
        high_similar_opposing_result = self.total_calculation(
            seq=away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high,
            percent=percent)
        low_similar_current_result = self.total_calculation(
            seq=home_structure.similar_command_individual_total_current_home_command_in_home_away_games_low,
            percent=percent)
        low_similar_opposing_result = self.total_calculation(
            seq=away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low,
            percent=percent)
        last_20_current_result = self.total_calculation(
            seq=home_structure.last_20_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)
        last_20_opposing_result = self.total_calculation(
            seq=away_structure.last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)
        last_12_current_result = self.total_calculation(
            seq=home_structure.last_12_games_individual_total_current_home_by_year_in_home_games,
            percent=percent)
        last_12_opposing_result = self.total_calculation(
            seq=away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games,
            percent=percent)
        last_8_current_result = self.total_calculation(
            seq=home_structure.last_8_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)
        last_8_opposing_result = self.total_calculation(
            seq=away_structure.last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)
        last_4_current_result = self.total_calculation(
            seq=home_structure.last_4_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)
        last_4_opposing_result = self.total_calculation(
            seq=away_structure.last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)

        big_data_current_under, big_data_current_over = big_data_current_result
        big_data_opposing_under, big_data_opposing_over = big_data_opposing_result
        last_year_current_under, last_year_current_over = last_year_current_result
        last_year_opposing_under, last_year_opposing_over = last_year_opposing_result
        h_similar_current_under, h_similar_current_over = high_similar_current_result
        h_similar_opposing_under, h_similar_opposing_over = high_similar_opposing_result
        l_similar_current_under, l_similar_current_over = low_similar_current_result
        l_similar_opposing_under, l_similar_opposing_over = low_similar_opposing_result
        last_20_current_under, last_20_current_over = last_20_current_result
        last_20_opposing_under, last_20_opposing_over = last_20_opposing_result
        last_12_current_under, last_12_current_over = last_12_current_result
        last_12_opposing_under, last_12_opposing_over = last_12_opposing_result
        last_8_current_under, last_8_current_over = last_8_current_result
        last_8_opposing_under, last_8_opposing_over = last_8_opposing_result
        last_4_current_under, last_4_current_over = last_4_current_result
        last_4_opposing_under, last_4_opposing_over = last_4_opposing_result

        under_list = [
            big_data_current_under,
            big_data_opposing_under,
            last_year_current_under,
            last_year_opposing_under,
            h_similar_current_under,
            h_similar_opposing_under,
            l_similar_current_under,
            l_similar_opposing_under,
            last_20_current_under,
            last_20_opposing_under,
            last_12_current_under,
            last_12_opposing_under,
            last_8_current_under,
            last_8_opposing_under,
            last_4_current_under,
            last_4_opposing_under
        ]

        over_list = [
            big_data_current_over,
            big_data_opposing_over,
            last_year_current_over,
            last_year_opposing_over,
            h_similar_current_over,
            h_similar_opposing_over,
            l_similar_current_over,
            l_similar_opposing_over,
            last_20_current_over,
            last_20_opposing_over,
            last_12_current_over,
            last_12_opposing_over,
            last_8_current_over,
            last_8_opposing_over,
            last_4_current_over,
            last_4_opposing_over,
        ]

        under = self.over_under_define(seq=under_list, over_under='under')
        over = self.over_under_define(seq=over_list, over_under='over')
        return under, over

    def calculate_individual_2_live_data(self, home_structure, away_structure, percent):
        big_data_current_result = self.total_calculation(
            seq=away_structure.big_data_individual_total_current_away_in_home_away_games,
            percent=percent)
        big_data_opposing_result = self.total_calculation(
            seq=home_structure.big_data_individual_total_opposing_teams_current_home_in_home_away_games,
            percent=percent)
        last_year_current_result = self.total_calculation(
            seq=away_structure.last_year_individual_total_current_away_command_in_home_away_games,
            percent=percent)
        last_year_opposing_result = self.total_calculation(
            seq=home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games,
            percent=percent)
        high_similar_current_result = self.total_calculation(
            seq=away_structure.similar_command_individual_total_current_away_command_in_home_away_games_high,
            percent=percent)
        high_similar_opposing_result = self.total_calculation(
            seq=home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high,
            percent=percent)
        low_similar_current_result = self.total_calculation(
            seq=away_structure.similar_command_individual_total_current_away_command_in_home_away_games_low,
            percent=percent)
        low_similar_opposing_result = self.total_calculation(
            seq=home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low,
            percent=percent)
        last_20_current_result = self.total_calculation(
            seq=away_structure.last_20_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)
        last_20_opposing_result = self.total_calculation(
            seq=home_structure.last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)
        last_12_current_result = self.total_calculation(
            seq=away_structure.last_12_games_individual_total_current_away_by_year_in_away_games,
            percent=percent)
        last_12_opposing_result = self.total_calculation(
            seq=home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games,
            percent=percent)
        last_8_current_result = self.total_calculation(
            seq=away_structure.last_8_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)
        last_8_opposing_result = self.total_calculation(
            seq=home_structure.last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)
        last_4_current_result = self.total_calculation(
            seq=away_structure.last_4_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)
        last_4_opposing_result = self.total_calculation(
            seq=home_structure.last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)

        big_data_current_under, big_data_current_over = big_data_current_result
        big_data_opposing_under, big_data_opposing_over = big_data_opposing_result
        last_year_current_under, last_year_current_over = last_year_current_result
        last_year_opposing_under, last_year_opposing_over = last_year_opposing_result
        h_similar_current_under, h_similar_current_over = high_similar_current_result
        h_similar_opposing_under, h_similar_opposing_over = high_similar_opposing_result
        l_similar_current_under, l_similar_current_over = low_similar_current_result
        l_similar_opposing_under, l_similar_opposing_over = low_similar_opposing_result
        last_20_current_under, last_20_current_over = last_20_current_result
        last_20_opposing_under, last_20_opposing_over = last_20_opposing_result
        last_12_current_under, last_12_current_over = last_12_current_result
        last_12_opposing_under, last_12_opposing_over = last_12_opposing_result
        last_8_current_under, last_8_current_over = last_8_current_result
        last_8_opposing_under, last_8_opposing_over = last_8_opposing_result
        last_4_current_under, last_4_current_over = last_4_current_result
        last_4_opposing_under, last_4_opposing_over = last_4_opposing_result

        under_list = [
            big_data_current_under,
            big_data_opposing_under,
            last_year_current_under,
            last_year_opposing_under,
            h_similar_current_under,
            h_similar_opposing_under,
            l_similar_current_under,
            l_similar_opposing_under,
            last_20_current_under,
            last_20_opposing_under,
            last_12_current_under,
            last_12_opposing_under,
            last_8_current_under,
            last_8_opposing_under,
            last_4_current_under,
            last_4_opposing_under
        ]

        over_list = [
            big_data_current_over,
            big_data_opposing_over,
            last_year_current_over,
            last_year_opposing_over,
            h_similar_current_over,
            h_similar_opposing_over,
            l_similar_current_over,
            l_similar_opposing_over,
            last_20_current_over,
            last_20_opposing_over,
            last_12_current_over,
            last_12_opposing_over,
            last_8_current_over,
            last_8_opposing_over,
            last_4_current_over,
            last_4_opposing_over,
        ]

        under = self.over_under_define(seq=under_list, over_under='under')
        over = self.over_under_define(seq=over_list, over_under='over')
        return under, over
