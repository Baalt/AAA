from line.analytics.live_utils.core import BoundaryLiveValues


class LiveHandicapCalculation(BoundaryLiveValues):
    def calculate_handicap_1_live_data(self, home_structure, away_structure, percent):
        big_data_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.big_data_individual_total_current_home_in_home_away_games,
            opposing_seq=home_structure.big_data_individual_total_opposing_teams_current_home_in_home_away_games,
            percent=percent)
        big_data_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.big_data_individual_total_opposing_teams_current_away_in_home_away_games,
            opposing_seq=away_structure.big_data_individual_total_current_away_in_home_away_games,
            percent=percent)
        last_year_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_year_individual_total_current_home_command_in_home_away_games,
            opposing_seq=home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games,
            percent=percent)
        last_year_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games,
            opposing_seq=away_structure.last_year_individual_total_current_away_command_in_home_away_games,
            percent=percent)
        last_20_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_20_games_individual_total_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)
        last_20_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_20_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)
        last_12_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_12_games_individual_total_current_home_by_year_in_home_games,
            opposing_seq=home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games,
            percent=percent)
        last_12_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games,
            opposing_seq=away_structure.last_12_games_individual_total_current_away_by_year_in_away_games,
            percent=percent)
        last_8_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_8_games_individual_total_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)
        last_8_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_8_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)
        last_4_current_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_4_games_individual_total_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            percent=percent)
        last_4_opposing_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_4_games_individual_total_current_away_by_year_in_home_away_games,
            percent=percent)

        handicap_list = [
            big_data_current_smart_handicap,
            big_data_opposing_smart_handicap,
            last_year_current_smart_handicap,
            last_year_opposing_smart_handicap,
            last_20_current_smart_handicap,
            last_20_opposing_smart_handicap,
            last_12_current_smart_handicap,
            last_12_opposing_smart_handicap,
            last_8_current_smart_handicap,
            last_8_opposing_smart_handicap,
            last_4_current_smart_handicap,
            last_4_opposing_smart_handicap
        ]
        return self.handicap_define(seq=handicap_list)

    def calculate_handicap_2_live_data(self, home_structure, away_structure, percent):
        big_data_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.big_data_individual_total_current_away_in_home_away_games,
            opposing_seq=away_structure.big_data_individual_total_opposing_teams_current_away_in_home_away_games,
            percent=percent)
        big_data_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.big_data_individual_total_opposing_teams_current_home_in_home_away_games,
            opposing_seq=home_structure.big_data_individual_total_current_home_in_home_away_games,
            percent=percent)
        last_year_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_year_individual_total_current_away_command_in_home_away_games,
            opposing_seq=away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games,
            percent=percent)
        last_year_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games,
            opposing_seq=home_structure.last_year_individual_total_current_home_command_in_home_away_games,
            percent=percent)
        last_20_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_20_games_individual_total_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)
        last_20_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_20_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)
        last_12_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_12_games_individual_total_current_away_by_year_in_away_games,
            opposing_seq=away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games,
            percent=percent)
        last_12_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games,
            opposing_seq=home_structure.last_12_games_individual_total_current_home_by_year_in_home_games,
            percent=percent)
        last_8_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_8_games_individual_total_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)
        last_8_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_8_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)
        last_4_current_smart_handicap = self.handicap_calculation(
            current_seq=away_structure.last_4_games_individual_total_current_away_by_year_in_home_away_games,
            opposing_seq=away_structure.last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games,
            percent=percent)
        last_4_opposing_smart_handicap = self.handicap_calculation(
            current_seq=home_structure.last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games,
            opposing_seq=home_structure.last_4_games_individual_total_current_home_by_year_in_home_away_games,
            percent=percent)

        handicap_list = [
            big_data_current_smart_handicap,
            big_data_opposing_smart_handicap,
            last_year_current_smart_handicap,
            last_year_opposing_smart_handicap,
            last_20_current_smart_handicap,
            last_20_opposing_smart_handicap,
            last_12_current_smart_handicap,
            last_12_opposing_smart_handicap,
            last_8_current_smart_handicap,
            last_8_opposing_smart_handicap,
            last_4_current_smart_handicap,
            last_4_opposing_smart_handicap
        ]
        return self.handicap_define(seq=handicap_list)
