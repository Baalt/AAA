import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.ioff()


class ScatterPlotBuilder:
    def __init__(self, matrix_data):
        self.matrix_data = matrix_data

    def build_scatter_plot(self, stat_name, bookmaker_value, bet_direction, season):
        if season == "current_season" or season == "year_current_season":
            filtered_teams = [
                team for team in self.matrix_data
                if team['current_position'] is not None # and (
                #             team['home_collections'][stat_name]['total'] or team['away_collections'][stat_name][
                #         'total'])
            ]
            sorted_teams = sorted(filtered_teams, key=lambda x: int(x['current_position']))
        elif season == "previous_season" or season == 'year_previous_season':
            filtered_teams = [
                team for team in self.matrix_data
                if team['previous_position'] is not None # and (
                #             team['home_collections'][stat_name]['total'] or team['away_collections'][stat_name][
                #         'total'])
            ]
            sorted_teams = sorted(filtered_teams, key=lambda x: int(x['previous_position']))
        else:
            raise ValueError("Invalid season")

        fig, ax = plt.subplots(figsize=(10, 6))

        x_offset = 0.2  # Adjust this value to control the separation between dots
        point_size = 50  # Adjust this value to control the size of the points

        for i, team in enumerate(sorted_teams):
            x = i  # Use the index as the x-coordinate

            if bet_direction in ['TO', 'TU']:
                y_home = team['home_collections'][stat_name]['total']
                y_away = team['away_collections'][stat_name]['total']
            elif bet_direction in ['TU_1', 'TO_1']:
                y_home = team['home_collections'][stat_name]['ind']
                y_away = team['away_collections'][stat_name]['ind_opp']
            elif bet_direction in ['TU_2', 'TO_2']:
                y_home = team['away_collections'][stat_name]['ind']
                y_away = team['home_collections'][stat_name]['ind_opp']
            elif bet_direction == 'H1':
                y_home = [value + bookmaker_value for value in team['home_collections'][stat_name]['hand']]
                y_away = [value + bookmaker_value for value in team['away_collections'][stat_name]['hand_opp']]
            elif bet_direction == 'H2':
                y_home = [value + bookmaker_value for value in team['away_collections'][stat_name]['hand']]
                y_away = [value + bookmaker_value for value in team['home_collections'][stat_name]['hand_opp']]
            else:
                raise ValueError("Invalid bet_direction")

            # Apply offset to x-coordinate for visual separation
            x_home = x - x_offset
            x_away = x + x_offset

            ax.scatter([x_home] * len(y_home), y_home, color='blue', marker='o', s=point_size, alpha=0.5)
            ax.scatter([x_away] * len(y_away), y_away, color='red', marker='o', s=point_size, alpha=0.5)

        if bet_direction in ['H1', 'H2']:
            ax.axhline(y=0, color='red', linewidth=2)  # Set the red line to y=0 for H1 and H2
        else:
            ax.axhline(y=bookmaker_value, color='red', linewidth=2)

        ax.set_xticks(range(len(sorted_teams)))
        ax.set_xticklabels([team['team_name'] for team in sorted_teams], rotation=90)
        ax.set_xlabel('Teams')
        ax.set_ylabel(stat_name)
        ax.set_title(f'{stat_name} - {bet_direction} - {season}')
        plt.tight_layout()

        fig.savefig(f"graph/data/{season}_stat.png", dpi=300)
        plt.close(fig)
