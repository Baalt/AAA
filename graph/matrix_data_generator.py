from utils.stat_switcher import stats_dict


class MatrixDataGenerator:
    def __init__(self, league_data, big_data, home_command_name: str, away_command_name):
        self.league_data = league_data
        self.big_data = big_data
        self.home_command_name = home_command_name[:10]
        self.away_command_name = away_command_name[:10]

    def generate_matrix_data(self):
        matrix_data = self.__process_league_data()
        matrix_data = self.__process_last_year_data(matrix_data)
        matrix_data = self.__combining_data(matrix_data)
        matrix_data = self.__modify_team_names(matrix_data)
        matrix_data = self.__reset_excess_matrix_data(matrix_data)
        return matrix_data

    def __process_league_data(self):
        matrix_data = []

        current_season_goals = self.league_data['current_season']['goals']
        previous_season_goals = self.league_data['previous_season']['goals']

        teams = set()
        for goal_data in current_season_goals:
            teams.add(goal_data['team_name'][:10])
        for goal_data in previous_season_goals:
            if goal_data['team_name'][:10] not in teams:
                teams.add(goal_data['team_name'][:10])


        for team_name in teams:
            matrix_entry = {
                'team_name': team_name,
                'current_position': None,
                'previous_position': None,
                'current_points': None,
                'previous_points': None,
                'current_games_played': None,
                'previous_games_played': None,
            }

            for goal_data in current_season_goals:
                if team_name in goal_data['team_name']:
                    matrix_entry['current_position'] = goal_data['team_position']
                    matrix_entry['current_points'] = goal_data['points']
                    matrix_entry['current_games_played'] = goal_data['games_played']

            for goal_data in previous_season_goals:
                if team_name in goal_data['team_name']:
                    matrix_entry['previous_position'] = goal_data['team_position']
                    matrix_entry['previous_points'] = goal_data['points']
                    matrix_entry['previous_games_played'] = goal_data['games_played']

            matrix_data.append(matrix_entry)

        return matrix_data

    def __process_last_year_data(self, matrix_data):
        primary_keys = list(self.big_data.keys())  # Primary keys like 'Goals', 'Fouls', etc.

        for matrix_entry in matrix_data:
            matrix_entry['home_collections'] = {}
            matrix_entry['away_collections'] = {}

            for primary_key in primary_keys:
                if not primary_key.startswith('home') and not primary_key.startswith('away'):
                    matrix_entry['home_collections'][stats_dict[primary_key]] = {
                        'total': [],
                        'ind': [],
                        'ind_opp': [],
                        'hand': [],
                        'hand_opp': []
                    }
                    matrix_entry['away_collections'][stats_dict[primary_key]] = {
                        'total': [],
                        'ind': [],
                        'ind_opp': [],
                        'hand': [],
                        'hand_opp': []
                    }
        return matrix_data

    def __combining_data(self, matrix_data):
        primary_keys = list(self.big_data.keys())  # Primary keys like 'Goals', 'Fouls', etc.

        for primary_key in primary_keys:
            if not primary_key.startswith('home') and not primary_key.startswith('away'):
                home_collections = self.big_data[primary_key]['home_collections']
                away_collections = self.big_data[primary_key]['away_collections']

                for matrix_entry in matrix_data:
                    team_name = matrix_entry['team_name']

                    home_command_data = [item for item in home_collections if
                                         team_name in item['home_command'] or team_name in item['away_command']]
                    away_command_data = [item for item in away_collections if
                                         team_name in item['home_command'] or team_name in item['away_command']]

                    home_total = []
                    home_ind = []
                    home_ind_opp = []
                    home_hand = []
                    home_hand_opp = []

                    for data in home_command_data:
                        home_total.append(
                            float(data['home_command_individual_total']) +
                            float(data['away_command_individual_total'])
                        )
                        home_ind.append(float(data['away_command_individual_total']) if team_name in data[
                            'home_command'] else float(data['home_command_individual_total']))
                        home_ind_opp.append(float(data['home_command_individual_total']) if team_name in data[
                            'home_command'] else float(data['away_command_individual_total']))
                        home_hand.append(
                            float(data['away_command_individual_total']) -
                            float(data['home_command_individual_total']) if team_name in data[
                                'home_command'] else float(data['home_command_individual_total']) -
                                                     float(data['away_command_individual_total']))

                        home_hand_opp.append(
                            float(data['home_command_individual_total']) -
                            float(data['away_command_individual_total']) if team_name in team_name in data[
                                'home_command'] else float(data['away_command_individual_total']) -
                                                     float(data['home_command_individual_total']))
                    away_total = []
                    away_ind = []
                    away_ind_opp = []
                    away_hand = []
                    away_hand_opp = []

                    for data in away_command_data:
                        away_total.append(
                            float(data['home_command_individual_total']) +
                            float(data['away_command_individual_total']))
                        away_ind.append(float(data['away_command_individual_total']) if team_name in data[
                            'home_command'] else float(data['home_command_individual_total']))
                        away_ind_opp.append(float(data['home_command_individual_total']) if team_name in data[
                            'home_command'] else float(data['away_command_individual_total']))
                        away_hand.append(
                            float(data['away_command_individual_total']) -
                            float(data['home_command_individual_total']) if team_name in data['home_command']
                            else float(data['home_command_individual_total']) -
                                 float(data['away_command_individual_total']))

                        away_hand_opp.append(
                            float(data['home_command_individual_total']) -
                            float(data['away_command_individual_total']) if team_name in data['home_command']
                            else float(data['away_command_individual_total']) -
                                 float(data['home_command_individual_total']))

                        matrix_entry['home_collections'][stats_dict[primary_key]]['total'] = home_total
                        matrix_entry['home_collections'][stats_dict[primary_key]]['ind'] = home_ind
                        matrix_entry['home_collections'][stats_dict[primary_key]]['ind_opp'] = home_ind_opp
                        matrix_entry['home_collections'][stats_dict[primary_key]]['hand'] = home_hand
                        matrix_entry['home_collections'][stats_dict[primary_key]]['hand_opp'] = home_hand_opp

                        matrix_entry['away_collections'][stats_dict[primary_key]]['total'] = away_total
                        matrix_entry['away_collections'][stats_dict[primary_key]]['ind'] = away_ind
                        matrix_entry['away_collections'][stats_dict[primary_key]]['ind_opp'] = away_ind_opp
                        matrix_entry['away_collections'][stats_dict[primary_key]]['hand'] = away_hand
                        matrix_entry['away_collections'][stats_dict[primary_key]]['hand_opp'] = away_hand_opp

        return matrix_data

    def __modify_team_names(self, matrix_data):
        modified_matrix_data = []

        for matrix_entry in matrix_data:
            team_name = matrix_entry['team_name']

            if self.home_command_name in team_name or team_name in self.home_command_name:
                modified_team_name = team_name.upper() + "_1"
            elif self.away_command_name in team_name or team_name in self.away_command_name:
                modified_team_name = team_name.upper() + "_2"
            else:
                modified_team_name = team_name

            matrix_entry['team_name'] = modified_team_name
            modified_matrix_data.append(matrix_entry)

        return modified_matrix_data

    def __reset_excess_matrix_data(self, matrix_data):
        for entry in matrix_data:
            team_name = entry['team_name']
            if team_name.endswith('_1'):
                home_collections = entry['home_collections']
                for key in home_collections:
                    home_collections[key] = {'hand': [], 'hand_opp': [], 'ind': [], 'ind_opp': [], 'total': []}

            elif team_name.endswith('_2'):
                away_collections = entry['away_collections']
                for key in away_collections:
                    away_collections[key] = {'hand': [], 'hand_opp': [], 'ind': [], 'ind_opp': [], 'total': []}

        return matrix_data
