from line.analytics.calc_utils.core import BoundaryLiveValues


class LiveTotalCalculation(BoundaryLiveValues):
    def calculate_total_live_data(self, home_structure, away_structure, percent):
        big_data_home_result = \
            self.total_calculation(seq=home_structure.big_data_total_current_home_in_home_away_games,
                                   percent=percent)
        big_data_away_result = \
            self.total_calculation(seq=away_structure.big_data_total_current_away_in_home_away_games,
                                   percent=percent)
        last_year_home_result = \
            self.total_calculation(seq=home_structure.last_year_total_current_home_command_in_home_away_games,
                                   percent=percent)
        last_year_away_result = \
            self.total_calculation(seq=away_structure.last_year_total_current_away_command_in_home_away_games,
                                   percent=percent)
        high_similar_home_result = \
            self.total_calculation(seq=home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                                   percent=percent)
        high_similar_away_result = \
            self.total_calculation(seq=away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                                   percent=percent)
        low_similar_home_result = \
            self.total_calculation(seq=home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                                   percent=percent)
        low_similar_away_result = \
            self.total_calculation(seq=away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                                   percent=percent)
        last_20_home_result = \
            self.total_calculation(seq=home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                                   percent=percent)
        last_20_away_result = \
            self.total_calculation(seq=away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                                   percent=percent)
        last_12_home_result = \
            self.total_calculation(seq=home_structure.last_12_games_total_current_home_command_by_year_in_home_games,
                                   percent=percent)
        last_12_away_result = \
            self.total_calculation(
                seq=away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12],
                percent=percent)
        last_8_home_result = \
            self.total_calculation(seq=home_structure.last_8_games_total_current_home_by_year_in_home_away_games,
                                   percent=percent)
        last_8_away_result = \
            self.total_calculation(seq=away_structure.last_8_games_total_current_away_by_year_in_home_away_games,
                                   percent=percent)
        last_4_home_result = \
            self.total_calculation(seq=home_structure.last_4_games_total_current_home_by_year_in_home_away_games,
                                   percent=percent)
        last_4_away_result = \
            self.total_calculation(seq=away_structure.last_4_games_total_current_away_by_year_in_home_away_games,
                                   percent=percent)

        big_data_home_under, big_data_home_over = big_data_home_result
        big_data_away_under, big_data_away_over = big_data_away_result
        last_year_home_under, last_year_home_over = last_year_home_result
        last_year_away_under, last_year_away_over = last_year_away_result
        h_similar_home_under, h_similar_home_over = high_similar_home_result
        l_similar_home_under, l_similar_home_over = low_similar_home_result
        h_similar_away_under, h_similar_away_over = high_similar_away_result
        l_similar_away_under, l_similar_away_over = low_similar_away_result

        last_20_home_under, last_20_home_over = last_20_home_result
        last_20_away_under, last_20_away_over = last_20_away_result
        last_12_home_under, last_12_home_over = last_12_home_result
        last_12_away_under, last_12_away_over = last_12_away_result
        last_8_home_under, last_8_home_over = last_8_home_result
        last_8_away_under, last_8_away_over = last_8_away_result
        last_4_home_under, last_4_home_over = last_4_home_result
        last_4_away_under, last_4_away_over = last_4_away_result

        under_list = [big_data_home_under,
                      big_data_away_under,
                      last_year_home_under,
                      last_year_away_under,
                      h_similar_home_under,
                      h_similar_away_under,
                      l_similar_home_under,
                      l_similar_away_under,
                      last_20_home_under,
                      last_20_away_under,
                      last_12_home_under,
                      last_12_away_under,
                      last_8_home_under,
                      last_8_away_under,
                      last_4_home_under,
                      last_4_away_under, ]

        over_list = [big_data_home_over,
                     big_data_away_over,
                     last_year_home_over,
                     last_year_away_over,
                     h_similar_home_over,
                     h_similar_away_over,
                     l_similar_home_over,
                     l_similar_away_over,
                     last_20_home_over,
                     last_20_away_over,
                     last_12_home_over,
                     last_12_away_over,
                     last_8_home_over,
                     last_8_away_over,
                     last_4_home_over,
                     last_4_away_over, ]

        under = self.over_under_define(seq=under_list, over_under='under')
        over = self.over_under_define(seq=over_list, over_under='over')
        return under, over
