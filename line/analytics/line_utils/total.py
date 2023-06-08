from line.analytics.line_utils.core import Catcher


class TotalCatcher(Catcher):
    async def search_total_rate(self, statistic_name: str, league_name: str):
        for coeff_set in self.coefficients[statistic_name]['total&coefficient']:
            big_data_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          big_data_total_current_home_in_home_away_games)
            big_data_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          big_data_total_current_away_in_home_away_games)
            last_year_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          last_year_total_current_home_command_in_home_away_games)
            last_year_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          last_year_total_current_away_command_in_home_away_games)
            tu_similar_home_result_low = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          similar_command_total_current_home_big_data_home_away_games_low)
            tu_similar_away_result_low = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          similar_command_total_current_away_big_data_home_away_games_low)
            tu_similar_home_result_high = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          similar_command_total_current_home_big_data_home_away_games_high)
            tu_similar_away_result_high = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          similar_command_total_current_away_big_data_home_away_games_high)
            to_similar_home_result_low = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          similar_command_total_current_home_big_data_home_away_games_low)
            to_similar_away_result_low = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          similar_command_total_current_away_big_data_home_away_games_low)
            to_similar_home_result_high = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          similar_command_total_current_home_big_data_home_away_games_high)
            to_similar_away_result_high = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          similar_command_total_current_away_big_data_home_away_games_high)
            last_20_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          last_20_games_total_current_home_by_year_in_home_away_games)
            last_20_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          last_20_games_total_current_away_by_year_in_home_away_games)
            last_12_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          last_12_games_total_current_home_command_by_year_in_home_games)
            last_12_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          last_12_games_total_current_away_command_by_year_in_away_games[:12])
            last_8_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          last_8_games_total_current_home_by_year_in_home_away_games)
            last_8_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          last_8_games_total_current_away_by_year_in_home_away_games)
            last_4_home_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.home_structure.
                                          last_4_games_total_current_home_by_year_in_home_away_games)
            last_4_away_result = \
                self.calculate_percentage(coeff_set=coeff_set,
                                          seq=self.away_structure.
                                          last_4_games_total_current_away_by_year_in_home_away_games)

            big_data_home_under_percent, big_data_home_over_percent = big_data_home_result
            big_data_away_under_percent, big_data_away_over_percent = big_data_away_result

            last_year_home_under_percent, last_year_home_over_percent = last_year_home_result
            last_year_away_under_percent, last_year_away_over_percent = last_year_away_result

            tu_similar_home_under_percent_low, similar_home_over_percent_low = tu_similar_home_result_low
            tu_similar_away_under_percent_low, similar_away_over_percent_low = tu_similar_away_result_low
            tu_similar_home_under_percent_high, similar_home_over_percent_high = tu_similar_home_result_high
            tu_similar_away_under_percent_high, similar_away_over_percent_high = tu_similar_away_result_high

            similar_home_under_percent_low, to_similar_home_over_percent_low = to_similar_home_result_low
            similar_away_under_percent, to_similar_away_over_percent_low = to_similar_away_result_low
            similar_home_under_percent_low, to_similar_home_over_percent_high = to_similar_home_result_high
            similar_away_under_percent, to_similar_away_over_percent_high = to_similar_away_result_high

            last_20_home_under_percent, last_20_home_over_percent = last_20_home_result
            last_20_away_under_percent, last_20_away_over_percent = last_20_away_result

            last_12_home_under_percent, last_12_home_over_percent = last_12_home_result
            last_12_away_under_percent, last_12_away_over_percent = last_12_away_result

            last_8_home_under_percent, last_8_home_over_percent = last_8_home_result
            last_8_away_under_percent, last_8_away_over_percent = last_8_away_result

            last_4_home_under_percent, last_4_home_over_percent = last_4_home_result
            last_4_away_under_percent, last_4_away_over_percent = last_4_away_result

            await self.search_kush_rate(statistic_name=statistic_name,
                                        league_name=league_name,
                                        coefficients=self.coefficients,
                                        coeff_set=coeff_set,
                                        rate_direction='Total_Under',
                                        coeff_under_over_key='coefficient_under',
                                        big_data_current_percent=big_data_home_under_percent,
                                        big_data_opposing_percent=big_data_away_under_percent,
                                        last_year_current_percent=last_year_home_under_percent,
                                        last_year_opposing_percent=last_year_away_under_percent,
                                        similar_current_percent_low=tu_similar_home_under_percent_low,
                                        similar_opposing_percent_low=tu_similar_away_under_percent_high,
                                        similar_current_percent_high=tu_similar_home_under_percent_high,
                                        similar_opposing_percent_high=tu_similar_away_under_percent_low,
                                        last_20_current_percent=last_20_home_under_percent,
                                        last_20_opposing_percent=last_20_away_under_percent,
                                        last_12_current_percent=last_12_home_under_percent,
                                        last_12_opposing_percent=last_12_away_under_percent,
                                        last_8_current_percent=last_8_home_under_percent,
                                        last_8_opposing_percent=last_8_away_under_percent,
                                        last_4_current_percent=last_4_home_under_percent,
                                        last_4_opposing_percent=last_4_away_under_percent)

            await self.search_kush_rate(statistic_name=statistic_name,
                                        league_name=league_name,
                                        coefficients=self.coefficients,
                                        coeff_set=coeff_set,
                                        rate_direction='Total_Over',
                                        coeff_under_over_key='coefficient_over',
                                        big_data_current_percent=big_data_home_over_percent,
                                        big_data_opposing_percent=big_data_away_over_percent,
                                        last_year_current_percent=last_year_home_over_percent,
                                        last_year_opposing_percent=last_year_away_over_percent,
                                        similar_current_percent_low=to_similar_home_over_percent_low,
                                        similar_opposing_percent_low=to_similar_away_over_percent_high,
                                        similar_current_percent_high=to_similar_home_over_percent_high,
                                        similar_opposing_percent_high=to_similar_away_over_percent_low,
                                        last_20_current_percent=last_20_home_over_percent,
                                        last_20_opposing_percent=last_20_away_over_percent,
                                        last_12_current_percent=last_12_home_over_percent,
                                        last_12_opposing_percent=last_12_away_over_percent,
                                        last_8_current_percent=last_8_home_over_percent,
                                        last_8_opposing_percent=last_8_away_over_percent,
                                        last_4_current_percent=last_4_home_over_percent,
                                        last_4_opposing_percent=last_4_away_over_percent)
