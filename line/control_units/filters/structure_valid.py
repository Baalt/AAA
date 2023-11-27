from line.analytics.structures import HomeDataStructure, AwayDataStructure


class ValidStructureFilter:
    def __init__(self, home_structure: HomeDataStructure, away_structure: AwayDataStructure):
        self.home_structure = home_structure
        self.away_structure = away_structure

    def valid_and_create(self):
        if self.is_home_structure_valid() and self.is_away_structure_valid():
            self.adding_home_structures_for_the_latest_games()
            self.adding_away_structures_for_the_latest_games()

    def adding_home_structures_for_the_latest_games(self):
        # last20 home-away games
        self.home_structure.last_20_games_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_total_current_home_command_in_home_away_games[:15]
        self.home_structure.last_20_games_individual_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_current_home_command_in_home_away_games[:15]
        self.home_structure.last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games[:15]
        # last 12 home games
        self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games = \
            self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:10]
        self.home_structure.last_12_games_individual_total_current_home_by_year_in_home_games = \
            self.home_structure.last_12_games_individual_total_current_home_by_year_in_home_games[:10]
        self.home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games = \
            self.home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games[:10]
        # last8 home-away games
        self.home_structure.last_8_games_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_total_current_home_command_in_home_away_games[:10]
        self.home_structure.last_8_games_individual_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_current_home_command_in_home_away_games[:10]
        self.home_structure.last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games[:10]
        # last4 home-away games
        self.home_structure.last_4_games_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_total_current_home_command_in_home_away_games[:5]
        self.home_structure.last_4_games_individual_total_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_current_home_command_in_home_away_games[:5]
        self.home_structure.last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = \
            self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games[:5]

    def adding_away_structures_for_the_latest_games(self):
        # last20 home-away games
        self.away_structure.last_20_games_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_total_current_away_command_in_home_away_games[:15]
        self.away_structure.last_20_games_individual_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_current_away_command_in_home_away_games[:15]
        self.away_structure.last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games[
            :15]
        # last12 away games
        self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games = \
            self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:10]
        self.away_structure.last_12_games_individual_total_current_away_by_year_in_away_games = \
            self.away_structure.last_12_games_individual_total_current_away_by_year_in_away_games[:10]
        self.away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games = \
            self.away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games[:10]
        # last8 home-away games
        self.away_structure.last_8_games_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_total_current_away_command_in_home_away_games[:10]
        self.away_structure.last_8_games_individual_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_current_away_command_in_home_away_games[:10]
        self.away_structure.last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games[:10]
        # last4 home-away games
        self.away_structure.last_4_games_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_total_current_away_command_in_home_away_games[:5]
        self.away_structure.last_4_games_individual_total_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_current_away_command_in_home_away_games[:5]
        self.away_structure.last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = \
            self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games[:5]

    def is_home_structure_valid(self):
        if self.home_structure:
            if len(self.home_structure.last_year_total_current_home_command_in_home_away_games) == len(
                    self.home_structure.last_year_individual_total_current_home_command_in_home_away_games) == len(
                self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games):

                if len(self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games) == len(
                        self.home_structure.last_12_games_individual_total_current_home_by_year_in_home_games) == len(
                    self.home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games):

                    if len(self.home_structure.last_year_total_current_home_command_in_home_away_games) >= 15 \
                            and len(
                        self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games) >= 10:
                        return True

    def is_away_structure_valid(self):
        if self.away_structure:
            if len(self.away_structure.last_year_total_current_away_command_in_home_away_games) == len(
                    self.away_structure.last_year_individual_total_current_away_command_in_home_away_games) == len(
                self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games):

                if len(self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games) == len(
                        self.away_structure.last_12_games_individual_total_current_away_by_year_in_away_games) == len(
                    self.away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games):

                    if len(self.away_structure.last_year_total_current_away_command_in_home_away_games) >= 15 \
                            and len(
                        self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games) >= 10:
                        return True


    def is_championships_home_structure_valid(self):
        if self.home_structure:
            if len(self.home_structure.last_year_total_current_home_command_in_home_away_games) == len(
                    self.home_structure.last_year_individual_total_current_home_command_in_home_away_games) == len(
                self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games):

                if len(self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games) == len(
                        self.home_structure.last_12_games_individual_total_current_home_by_year_in_home_games) == len(
                    self.home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games):

                    if len(self.home_structure.big_data_total_current_home_in_home_away_games) >= 7 \
                            and len(
                        self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games) >= 3:
                        return True

    def is_championships_away_structure_valid(self):
        if self.away_structure:
            if len(self.away_structure.last_year_total_current_away_command_in_home_away_games) == len(
                    self.away_structure.last_year_individual_total_current_away_command_in_home_away_games) == len(
                self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games):

                if len(self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games) == len(
                        self.away_structure.last_12_games_individual_total_current_away_by_year_in_away_games) == len(
                    self.away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games):

                    if len(self.away_structure.big_data_total_current_away_in_home_away_games) >= 7 \
                            and len(
                        self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games) >= 4:
                        return True