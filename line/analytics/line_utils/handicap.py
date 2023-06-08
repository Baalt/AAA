from line.analytics.line_utils.core import Catcher


class HandicapCatcher(Catcher):
    async def search_handicap_1_rate(self, statistic_name: str, league_name: str):
        for coeff_set in self.coefficients[statistic_name]['handicap_1_&coefficient']:
            big_data_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                big_data_individual_total_current_home_in_home_away_games,
                opposing_seq=self.home_structure.
                big_data_individual_total_opposing_teams_current_home_in_home_away_games)
            big_data_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                big_data_individual_total_opposing_teams_current_away_in_home_away_games,
                opposing_seq=self.away_structure.
                big_data_individual_total_current_away_in_home_away_games)
            last_year_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_year_individual_total_current_home_command_in_home_away_games,
                opposing_seq=self.home_structure.
                last_year_individual_total_opposing_teams_current_home_in_home_away_games)
            last_year_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_year_individual_total_opposing_teams_current_away_in_home_away_games,
                opposing_seq=self.away_structure.
                last_year_individual_total_current_away_command_in_home_away_games)
            similar_current_percent_low = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                similar_command_individual_total_current_home_command_in_home_away_games_low,
                opposing_seq=self.home_structure.
                similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low)
            similar_current_percent_high = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                similar_command_individual_total_current_home_command_in_home_away_games_high,
                opposing_seq=self.home_structure.
                similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high)
            similar_opposing_percent_low = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low,
                opposing_seq=self.away_structure.
                similar_command_individual_total_current_away_command_in_home_away_games_low)
            similar_opposing_percent_high = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high,
                opposing_seq=self.away_structure.
                similar_command_individual_total_current_away_command_in_home_away_games_high)
            last_20_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_20_games_individual_total_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games)
            last_20_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_20_games_individual_total_current_away_by_year_in_home_away_games)
            last_12_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_12_games_individual_total_current_home_by_year_in_home_games,
                opposing_seq=self.home_structure.
                last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games)
            last_12_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games,
                opposing_seq=self.away_structure.
                last_12_games_individual_total_current_away_by_year_in_away_games)
            last_8_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_8_games_individual_total_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games)
            last_8_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_8_games_individual_total_current_away_by_year_in_home_away_games)
            last_4_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_4_games_individual_total_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games)
            last_4_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_4_games_individual_total_current_away_by_year_in_home_away_games)

            await self.search_kush_rate(statistic_name=statistic_name,
                                        league_name=league_name,
                                        coefficients=self.coefficients,
                                        coeff_set=coeff_set,
                                        rate_direction='Handicap_1',
                                        coeff_under_over_key='coefficient',
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

    async def search_handicap_2_rate(self, statistic_name: str, league_name: str):
        for coeff_set in self.coefficients[statistic_name]['handicap_2_&coefficient']:
            big_data_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                big_data_individual_total_current_away_in_home_away_games,
                opposing_seq=self.away_structure.
                big_data_individual_total_opposing_teams_current_away_in_home_away_games)
            big_data_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                big_data_individual_total_opposing_teams_current_home_in_home_away_games,
                opposing_seq=self.home_structure.
                big_data_individual_total_current_home_in_home_away_games)
            last_year_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_year_individual_total_current_away_command_in_home_away_games,
                opposing_seq=self.away_structure.
                last_year_individual_total_opposing_teams_current_away_in_home_away_games)
            last_year_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_year_individual_total_opposing_teams_current_home_in_home_away_games,
                opposing_seq=self.home_structure.
                last_year_individual_total_current_home_command_in_home_away_games)
            similar_current_percent_low = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                similar_command_individual_total_current_away_command_in_home_away_games_low,
                opposing_seq=self.away_structure.
                similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low)
            similar_current_percent_high = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                similar_command_individual_total_current_away_command_in_home_away_games_high,
                opposing_seq=self.away_structure.
                similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high)
            similar_opposing_percent_low = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low,
                opposing_seq=self.home_structure.
                similar_command_individual_total_current_home_command_in_home_away_games_low)
            similar_opposing_percent_high = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high,
                opposing_seq=self.home_structure.
                similar_command_individual_total_current_home_command_in_home_away_games_high)
            last_20_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_20_games_individual_total_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games)
            last_20_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_20_games_individual_total_current_home_by_year_in_home_away_games)
            last_12_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_12_games_individual_total_current_away_by_year_in_away_games,
                opposing_seq=self.away_structure.
                last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games)
            last_12_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games,
                opposing_seq=self.home_structure.
                last_12_games_individual_total_current_home_by_year_in_home_games)
            last_8_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_8_games_individual_total_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games)
            last_8_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_8_games_individual_total_current_home_by_year_in_home_away_games)
            last_4_current_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.away_structure.
                last_4_games_individual_total_current_away_by_year_in_home_away_games,
                opposing_seq=self.away_structure.
                last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games)
            last_4_opposing_percent = self.handicap_percentage_calculate(
                coeff_set=coeff_set,
                current_seq=self.home_structure.
                last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
                opposing_seq=self.home_structure.
                last_4_games_individual_total_current_home_by_year_in_home_away_games)

            await self.search_kush_rate(statistic_name=statistic_name,
                                        league_name=league_name,
                                        coefficients=self.coefficients,
                                        coeff_set=coeff_set,
                                        rate_direction='Handicap_2',
                                        coeff_under_over_key='coefficient',
                                        big_data_current_percent=big_data_current_percent,
                                        big_data_opposing_percent=big_data_opposing_percent,
                                        last_year_current_percent=last_year_current_percent,
                                        last_year_opposing_percent=last_year_opposing_percent,
                                        similar_current_percent_low=similar_current_percent_low,
                                        similar_opposing_percent_low=similar_opposing_percent_high,
                                        similar_current_percent_high=similar_current_percent_high,
                                        similar_opposing_percent_high=similar_opposing_percent_low,
                                        last_20_current_percent=last_20_current_percent,
                                        last_20_opposing_percent=last_20_opposing_percent,
                                        last_12_current_percent=last_12_current_percent,
                                        last_12_opposing_percent=last_12_opposing_percent,
                                        last_8_current_percent=last_8_current_percent,
                                        last_8_opposing_percent=last_8_opposing_percent,
                                        last_4_current_percent=last_4_current_percent,
                                        last_4_opposing_percent=last_4_opposing_percent)
