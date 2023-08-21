class MatrixDataGenerator:
    def __init__(self, league_data, last_year_data, home_command_name: str, away_command_name):
        self.league_data = league_data
        self.last_year_data = last_year_data
        self.home_command_name = home_command_name[:10]
        self.away_command_name = away_command_name[:10]

    def generate_matrix_data(self):
        matrix_data = self.__process_league_data()
        matrix_data = self.__process_last_year_data(matrix_data)
        matrix_data = self.__combining_data(matrix_data)
        return matrix_data

    def __process_league_data(self):
        matrix_data = []

        current_season_goals = self.league_data['current_season']['goals']
        previous_season_goals = self.league_data['previous_season']['goals']

        teams = set()
        for goal_data in current_season_goals:
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
                if goal_data['team_name'] == team_name:
                    matrix_entry['current_position'] = goal_data['team_position']
                    matrix_entry['current_points'] = goal_data['points']
                    matrix_entry['current_games_played'] = goal_data['games_played']

            for goal_data in previous_season_goals:
                if goal_data['team_name'] == team_name:
                    matrix_entry['previous_position'] = goal_data['team_position']
                    matrix_entry['previous_points'] = goal_data['points']
                    matrix_entry['previous_games_played'] = goal_data['games_played']

            matrix_data.append(matrix_entry)

        return matrix_data

    def __process_last_year_data(self, matrix_data):
        primary_keys = list(self.last_year_data.keys())  # Primary keys like 'Goals', 'Fouls', etc.

        for primary_key in primary_keys:
            for matrix_entry in matrix_data:
                matrix_entry['home_collections'] = {
                    primary_key: {
                        'total': [],
                        'ind': [],
                        'hand': []
                    }
                }
                matrix_entry['away_collections'] = {
                    primary_key: {
                        'total': [],
                        'ind': [],
                        'hand': []
                    }
                }
        return matrix_data

    def __combining_data(self, matrix_data):
        primary_keys = list(self.last_year_data.keys())  # Primary keys like 'Goals', 'Fouls', etc.

        for primary_key in primary_keys:
            home_collections = self.last_year_data[primary_key]['home_collections']
            away_collections = self.last_year_data[primary_key]['away_collections']

            for matrix_entry in matrix_data:
                team_name = matrix_entry['team_name']

                home_command_data_1 = next(
                    (item for item in home_collections if team_name in item['home_command']), None
                )
                home_command_data_2 = next(
                    (item for item in home_collections if team_name in item['away_command']), None
                )

                away_command_data_1 = next(
                    (item for item in away_collections if team_name in item['away_command']), None
                )
                away_command_data_2 = next(
                    (item for item in away_collections if team_name in item['home_command']), None
                )

                if home_command_data_1:
                    matrix_entry['home_collections'][primary_key]['total'].append(
                        float(home_command_data_1['home_command_individual_total']) +
                        float(home_command_data_1['away_command_individual_total'])
                    )
                    matrix_entry['home_collections'][primary_key]['ind'].append(
                        float(home_command_data_1['away_command_individual_total'])
                    )
                    matrix_entry['home_collections'][primary_key]['hand'].append(
                        float(home_command_data_1['away_command_individual_total']) -
                        float(home_command_data_1['home_command_individual_total'])
                    )

                if home_command_data_2:
                    matrix_entry['home_collections'][primary_key]['total'].append(
                        float(home_command_data_2['home_command_individual_total']) +
                        float(home_command_data_2['away_command_individual_total'])
                    )
                    matrix_entry['home_collections'][primary_key]['ind'].append(
                        float(home_command_data_2['home_command_individual_total'])
                    )
                    matrix_entry['home_collections'][primary_key]['hand'].append(
                        float(home_command_data_2['home_command_individual_total']) -
                        float(home_command_data_2['away_command_individual_total'])
                    )

                if away_command_data_1:
                    matrix_entry['away_collections'][primary_key]['total'].append(
                        float(away_command_data_1['home_command_individual_total']) +
                        float(away_command_data_1['away_command_individual_total'])
                    )
                    matrix_entry['away_collections'][primary_key]['ind'].append(
                        float(away_command_data_1['home_command_individual_total'])
                    )
                    matrix_entry['away_collections'][primary_key]['hand'].append(
                        float(away_command_data_1['home_command_individual_total']) -
                        float(away_command_data_1['away_command_individual_total'])
                    )

                if away_command_data_2:
                    matrix_entry['away_collections'][primary_key]['total'].append(
                        float(away_command_data_2['home_command_individual_total']) +
                        float(away_command_data_2['away_command_individual_total'])
                    )
                    matrix_entry['away_collections'][primary_key]['ind'].append(
                        float(away_command_data_2['away_command_individual_total'])
                    )
                    matrix_entry['away_collections'][primary_key]['hand'].append(
                        float(away_command_data_2['away_command_individual_total']) -
                        float(away_command_data_2['home_command_individual_total'])
                    )

        return matrix_data