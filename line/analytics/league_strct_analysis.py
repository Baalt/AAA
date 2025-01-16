from utils.pickle_manager import PickleHandler


class LeaguePerformanceAnalyzer:
    def __init__(self, dct: dict):
        self.dct = dct
        self.result = {}

    def verify_games_played(self, league_name, stat_key='goals', min_games=8):
        if stat_key not in self.dct[league_name]:
            print(f"Ключ статистики '{stat_key}' не найден в лиге '{league_name}'.")
            return None
        stat_list = self.dct[league_name][stat_key]
        for record in stat_list:
            games_played = int(record.get('games_played'))
            if games_played < min_games:
                print(f"Недостаточно игр в : {league_name}")
                return None
        return True

    def categorize_teams(self, stat_list, avg_key):
        try:
            avg_values = [float(record.get(avg_key, 0)) for record in stat_list]
        except ValueError:
            return
        if not avg_values:
            return
        avg_mean = sum(avg_values) / len(avg_values)

        categories = {
            'more_25': [],
            'more_15-25': [],
            'more_5-15': [],
            'avg_5-5': [],
            'less_5-15': [],
            'less_15-25': [],
            'less_25': []
        }

        for record in stat_list:
            avg_value = float(record.get(avg_key, 0))
            team_name = record.get('team_name', 'Unknown')
            try:
                diff_percent = ((avg_value - avg_mean) / avg_mean) * 100
            except ZeroDivisionError:
                print(f'(({avg_value} - {avg_mean}) / {avg_mean}) * 100')
                continue

            if diff_percent >= 25:
                categories['more_25'].append(team_name)
            elif 15 <= diff_percent < 25:
                categories['more_15-25'].append(team_name)
            elif 5 <= diff_percent < 15:
                categories['more_5-15'].append(team_name)
            elif -5 <= diff_percent < 5:
                categories['avg_5-5'].append(team_name)
            elif -15 <= diff_percent < -5:
                categories['less_5-15'].append(team_name)
            elif -25 <= diff_percent < -15:
                categories['less_15-25'].append(team_name)
            elif diff_percent < -25:
                categories['less_25'].append(team_name)

        return categories

    def analyze_leagues(self):
        for league_name, league_data in self.dct.items():
            if not self.verify_games_played(league_name):
                continue

            self.result[league_name] = {}

            for stat_key, stat_list in league_data.items():
                if stat_key == 'goals':
                    avg_key = 'avg_individual_team'
                    categories = self.categorize_teams(stat_list, avg_key)
                    if categories is not None:
                        self.result[league_name][stat_key] = categories

                    avg_key = 'points'
                    categories = self.categorize_teams(stat_list, avg_key)
                    if categories is not None:
                        self.result[league_name]['position'] = categories

                elif stat_key in ['ref_yellow cards', 'ref_fouls']:
                    avg_key = 'avg_overall_total'
                    categories = self.categorize_teams(stat_list, avg_key)
                    if categories is not None:
                        self.result[league_name][stat_key] = categories
                else:
                    avg_key = 'avg_individual_team'
                    categories = self.categorize_teams(stat_list, avg_key)
                    if categories is not None:
                        self.result[league_name][stat_key] = categories

    def save_results(self, schedule_data):
        file_name = f"data/{schedule_data['date']}_AllLeaguesStructure.pkl"
        pickle_handler = PickleHandler()
        pickle_handler.write_data(self.result, file_name)
