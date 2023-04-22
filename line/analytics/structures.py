class HomeDataStructure:
    def __init__(self):
        # big data home-away
        self.big_data_total_current_home_in_home_away_games = list()
        self.big_data_individual_total_current_home_in_home_away_games = list()
        self.big_data_individual_total_opposing_teams_current_home_in_home_away_games = list()

        # big data similar commands
        self.similar_command_total_current_home_big_data_home_away_games_high = list()
        self.similar_command_individual_total_current_home_command_in_home_away_games_high = list()
        self.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high = list()

        self.similar_command_total_current_home_big_data_home_away_games_low = list()
        self.similar_command_individual_total_current_home_command_in_home_away_games_low = list()
        self.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low = list()

        # last year home-away
        self.last_year_total_current_home_command_in_home_away_games = list()
        self.last_year_individual_total_current_home_command_in_home_away_games = list()
        self.last_year_individual_total_opposing_teams_current_home_in_home_away_games = list()

        # last20 home-away games
        self.last_20_games_total_current_home_by_year_in_home_away_games = None
        self.last_20_games_individual_total_current_home_by_year_in_home_away_games = None
        self.last_20_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = None

        # last12 home games
        self.last_12_games_total_current_home_command_by_year_in_home_games = list()
        self.last_12_games_individual_total_current_home_by_year_in_home_games = list()
        self.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games = list()

        # last8 home-away games
        self.last_8_games_total_current_home_by_year_in_home_away_games = None
        self.last_8_games_individual_total_current_home_by_year_in_home_away_games = None
        self.last_8_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = None

        # last4 home-away games
        self.last_4_games_total_current_home_by_year_in_home_away_games = None
        self.last_4_games_individual_total_current_home_by_year_in_home_away_games = None
        self.last_4_games_individual_total_opposing_teams_current_home_by_year_in_home_away_games = None


class AwayDataStructure:
    def __init__(self):
        # big data home-away
        self.big_data_total_current_away_in_home_away_games = list()
        self.big_data_individual_total_current_away_in_home_away_games = list()
        self.big_data_individual_total_opposing_teams_current_away_in_home_away_games = list()

        # big data similar commands
        self.similar_command_total_current_away_big_data_home_away_games_high = list()
        self.similar_command_individual_total_current_away_command_in_home_away_games_high = list()
        self.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high = list()

        self.similar_command_total_current_away_big_data_home_away_games_low = list()
        self.similar_command_individual_total_current_away_command_in_home_away_games_low = list()
        self.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low = list()

        # last year home-away
        self.last_year_total_current_away_command_in_home_away_games = list()
        self.last_year_individual_total_current_away_command_in_home_away_games = list()
        self.last_year_individual_total_opposing_teams_current_away_in_home_away_games = list()

        # last20 home-away games
        self.last_20_games_total_current_away_by_year_in_home_away_games = None
        self.last_20_games_individual_total_current_away_by_year_in_home_away_games = None
        self.last_20_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = None

        # last12 away games
        self.last_12_games_total_current_away_command_by_year_in_away_games = list()
        self.last_12_games_individual_total_current_away_by_year_in_away_games = list()
        self.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games = list()

        # last8 home-away games
        self.last_8_games_total_current_away_by_year_in_home_away_games = None
        self.last_8_games_individual_total_current_away_by_year_in_home_away_games = None
        self.last_8_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = None

        # last4 home-away games
        self.last_4_games_total_current_away_by_year_in_home_away_games = None
        self.last_4_games_individual_total_current_away_by_year_in_home_away_games = None
        self.last_4_games_individual_total_opposing_teams_current_away_by_year_in_home_away_games = None


class FromDictToStructure:
    def clear_command_name(self,
                           command_name: str):
        if '(' in command_name:
            clean_command_name = command_name.split('(')
            if len(clean_command_name) == 2:
                return clean_command_name[0].strip()
        return command_name.strip()

    def convert(self,
                big_match_data: dict,
                last_year_data: dict,
                statistic_name: str,
                main_command_name: str,
                home_away_collection: str,
                similar_home_commands_list_high: list,
                similar_home_commands_list_low: list,
                similar_away_commands_list_high: list,
                similar_away_commands_list_low: list, ):

        if home_away_collection == 'home_collections':
            self.home_structure = HomeDataStructure()
        elif home_away_collection == 'away_collections':
            self.away_structure = AwayDataStructure()

        for match in big_match_data[statistic_name][home_away_collection]:
            match_home_command = self.clear_command_name(match['home_command'])
            match_away_command = self.clear_command_name(match['away_command'])
            if (main_command_name in match_home_command or match_home_command in main_command_name) or \
                    (main_command_name in match_away_command or match_away_command in main_command_name):
                try:
                    ind_home_total = int(match["home_command_individual_total"])
                    ind_away_total = int(match["away_command_individual_total"])
                    total = ind_home_total + ind_away_total

                except ValueError:
                    continue

                if home_away_collection == 'home_collections':
                    self.home_structure.big_data_total_current_home_in_home_away_games.append(total)
                    if main_command_name in match_home_command or match_home_command in main_command_name:
                        self.home_structure.big_data_individual_total_current_home_in_home_away_games.append(
                            ind_home_total)
                        self.home_structure.big_data_individual_total_opposing_teams_current_home_in_home_away_games.append(
                            ind_away_total)

                        for command in similar_away_commands_list_high:
                            if match_away_command in command or command in match_away_command:
                                self.home_structure.similar_command_total_current_home_big_data_home_away_games_high.append(
                                    total)
                                self.home_structure.similar_command_individual_total_current_home_command_in_home_away_games_high.append(
                                    ind_home_total)
                                self.home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high.append(
                                    ind_away_total)

                        for command in similar_away_commands_list_low:
                            if match_away_command in command or command in match_away_command:
                                self.home_structure.similar_command_total_current_home_big_data_home_away_games_low.append(
                                    total)
                                self.home_structure.similar_command_individual_total_current_home_command_in_home_away_games_low.append(
                                    ind_home_total)
                                self.home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low.append(
                                    ind_away_total)


                    elif main_command_name in match_away_command or match_away_command in main_command_name:
                        self.home_structure.big_data_individual_total_current_home_in_home_away_games.append(
                            ind_away_total)
                        self.home_structure.big_data_individual_total_opposing_teams_current_home_in_home_away_games.append(
                            ind_home_total)

                        for command in similar_away_commands_list_high:
                            if match_home_command in command or command in match_home_command:
                                self.home_structure.similar_command_total_current_home_big_data_home_away_games_high.append(
                                    total)
                                self.home_structure.similar_command_individual_total_current_home_command_in_home_away_games_high.append(
                                    ind_away_total)
                                self.home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_high.append(
                                    ind_home_total)

                        for command in similar_away_commands_list_low:
                            if match_home_command in command or command in match_home_command:
                                self.home_structure.similar_command_total_current_home_big_data_home_away_games_low.append(
                                    total)
                                self.home_structure.similar_command_individual_total_current_home_command_in_home_away_games_low.append(
                                    ind_away_total)
                                self.home_structure.similar_command_individual_total_opposing_teams_current_home_in_home_away_games_low.append(
                                    ind_home_total)


                elif home_away_collection == 'away_collections':
                    self.away_structure.big_data_total_current_away_in_home_away_games.append(total)
                    if main_command_name in match_home_command or match_home_command in main_command_name:
                        self.away_structure.big_data_individual_total_current_away_in_home_away_games.append(
                            ind_home_total)
                        self.away_structure.big_data_individual_total_opposing_teams_current_away_in_home_away_games.append(
                            ind_away_total)

                        for command in similar_home_commands_list_high:
                            if match_away_command in command or command in match_away_command:
                                self.away_structure.similar_command_total_current_away_big_data_home_away_games_high.append(
                                    total)
                                self.away_structure.similar_command_individual_total_current_away_command_in_home_away_games_high.append(
                                    ind_home_total)
                                self.away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high.append(
                                    ind_away_total)

                        for command in similar_home_commands_list_low:
                            if match_away_command in command or command in match_away_command:
                                self.away_structure.similar_command_total_current_away_big_data_home_away_games_low.append(
                                    total)
                                self.away_structure.similar_command_individual_total_current_away_command_in_home_away_games_low.append(
                                    ind_home_total)
                                self.away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low.append(
                                    ind_away_total)


                    elif main_command_name in match_away_command or match_away_command in main_command_name:
                        self.away_structure.big_data_individual_total_current_away_in_home_away_games.append(
                            ind_away_total)
                        self.away_structure.big_data_individual_total_opposing_teams_current_away_in_home_away_games.append(
                            ind_home_total)

                        for command in similar_home_commands_list_high:
                            if match_home_command in command or command in match_home_command:
                                self.away_structure.similar_command_total_current_away_big_data_home_away_games_high.append(
                                    total)
                                self.away_structure.similar_command_individual_total_current_away_command_in_home_away_games_high.append(
                                    ind_away_total)
                                self.away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_high.append(
                                    ind_home_total)

                        for command in similar_home_commands_list_low:
                            if match_home_command in command or command in match_home_command:
                                self.away_structure.similar_command_total_current_away_big_data_home_away_games_low.append(
                                    total)
                                self.away_structure.similar_command_individual_total_current_away_command_in_home_away_games_low.append(
                                    ind_away_total)
                                self.away_structure.similar_command_individual_total_opposing_teams_current_away_in_home_away_games_low.append(
                                    ind_home_total)

        for match in last_year_data[statistic_name][home_away_collection]:
            match_home_command = self.clear_command_name(match['home_command'])
            match_away_command = self.clear_command_name(match['away_command'])
            if (main_command_name in match_home_command or match_home_command in main_command_name) or \
                    (main_command_name in match_away_command or match_away_command in main_command_name):
                try:
                    ind_home_total = int(match["home_command_individual_total"])
                    ind_away_total = int(match["away_command_individual_total"])
                    total = ind_home_total + ind_away_total

                except ValueError:
                    continue

                if home_away_collection == 'home_collections':
                    self.home_structure.last_year_total_current_home_command_in_home_away_games.append(total)
                elif home_away_collection == 'away_collections':
                    self.away_structure.last_year_total_current_away_command_in_home_away_games.append(total)

                if main_command_name in match_home_command or match_home_command in main_command_name:
                    if home_away_collection == 'home_collections':
                        self.home_structure.last_year_individual_total_current_home_command_in_home_away_games.append(
                            ind_home_total)
                        self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games.append(
                            ind_away_total)

                        self.home_structure.last_12_games_total_current_home_command_by_year_in_home_games.append(
                            total)
                        self.home_structure.last_12_games_individual_total_current_home_by_year_in_home_games.append(
                            ind_home_total)
                        self.home_structure.last_12_games_individual_total_opposing_teams_current_home_by_year_in_away_games.append(
                            ind_away_total)


                    elif home_away_collection == 'away_collections':
                        self.away_structure.last_year_individual_total_current_away_command_in_home_away_games.append(
                            ind_home_total)
                        self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games.append(
                            ind_away_total)



                elif main_command_name in match_away_command or match_away_command in main_command_name:
                    if home_away_collection == 'home_collections':
                        self.home_structure.last_year_individual_total_current_home_command_in_home_away_games.append(
                            ind_away_total)
                        self.home_structure.last_year_individual_total_opposing_teams_current_home_in_home_away_games.append(
                            ind_home_total)

                    elif home_away_collection == 'away_collections':
                        self.away_structure.last_year_individual_total_current_away_command_in_home_away_games.append(
                            ind_away_total)
                        self.away_structure.last_year_individual_total_opposing_teams_current_away_in_home_away_games.append(
                            ind_home_total)

                        self.away_structure.last_12_games_total_current_away_command_by_year_in_away_games.append(
                            total)
                        self.away_structure.last_12_games_individual_total_current_away_by_year_in_away_games.append(
                            ind_away_total)
                        self.away_structure.last_12_games_individual_total_opposing_teams_current_away_by_year_in_home_games.append(
                            ind_home_total)

        if home_away_collection == 'home_collections':
            return self.home_structure

        elif home_away_collection == 'away_collections':
            return self.away_structure
