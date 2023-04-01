import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
plt.ioff()


class FootballStatsVisualizer:
    def __init__(self, data, team_name_1, team_name_2):
        self.data = data
        self.team_name_1 = team_name_1
        self.team_name_2 = team_name_2

    def plot_points(self, data_lst, season):
        team_names = []
        values = []

        for team in data_lst:
            team_data = []
            team_data.append(int(team['points']))
            team_data.append(int(team['games_played']))
            values.append(team_data)
            team_name = team['team_name']
            if self.team_name_1 in team_name:
                team_name = f"{team_name.upper()}_1"
            elif self.team_name_2 in team_name:
                team_name = f"{team_name.upper()}_2"
            team_names.append(team_name)

        values = np.array(values)
        num_bars = values.shape[1]

        plt.figure()
        plt.bar(np.arange(len(team_names)), values[:, 0], color='black')

        for i, value in enumerate(values):
            plt.text(i, value[0] + 2, f"{value[0]} / {value[1]}", ha='center', fontsize=13,
                     bbox=dict(facecolor='white', edgecolor='white', alpha=0.5, pad=1))

        plt.xticks(np.arange(len(team_names)), team_names, rotation=90, fontsize=10)
        plt.title(f'Points - {season}')
        plt.xlabel('Team')
        plt.ylabel('Points')
        plt.gcf().set_size_inches(24, 12)

        plt.savefig(f"graph/data/{season}_points.png")


    def plot_team_stats(self, stat_key, season, sort_by=None):
        team_names = []
        values = []

        if sort_by is not None:
            sorted_data = sorted(self.data[stat_key], key=lambda x: float(x[sort_by]), reverse=True)
        else:
            sorted_data = self.data[stat_key]

        for team in sorted_data:
            team_data = []
            team_data.append(float(team['avg_overall_total']))
            team_data.append(float(team['avg_individual_team']))
            team_data.append(float(team['avg_individual_team_against']))
            values.append(team_data)
            team_name = team['team_name']
            if self.team_name_1 in team_name:
                team_name = f"{team_name.upper()}_1"
            elif self.team_name_2 in team_name:
                team_name = f"{team_name.upper()}_2"
            team_names.append(team_name)

        values = np.array(values)
        num_bars = values.shape[1]

        colors = ['b', 'g', 'r']

        plt.figure()
        for i in range(num_bars):
            if i == 0:
                plt.bar(np.arange(len(team_names)) + i * 0.2, values[:, i], width=0.2, label='avg_overall_total',
                        color=colors[0], edgecolor='white')
            elif i == 1:
                plt.bar(np.arange(len(team_names)) + i * 0.2, values[:, i], width=0.2, label='avg_individual_team',
                        color=colors[1], edgecolor='white')
            elif i == 2:
                plt.bar(np.arange(len(team_names)) + i * 0.2, values[:, i], width=0.2, label='avg_individual_team_against',
                        color=colors[2], edgecolor='white')

            # Add bar labels above each bar with a white border
            plt.bar_label(
                plt.bar(np.arange(len(team_names)) + i * 0.2, values[:, i], width=0.2, color=colors[i], edgecolor='white'),
                labels=values[:, i], label_type='edge', fontsize=10, padding=3, color='black',
                bbox=dict(facecolor='white', edgecolor='white', alpha=0.5, pad=1)
            )

        # Set the axis labels, title, and legend
        plt.legend()
        plt.xticks(np.arange(len(team_names)), team_names, rotation=90, fontsize=10)  # Reduce tick label font size
        plt.title(f'{stat_key.capitalize()} - {season}')
        plt.xlabel('Team')
        plt.ylabel('Total')
        plt.gcf().set_size_inches(24, 12)

        # Save the graph as an image
        plt.savefig(f"graph/data/{season}_stat.png")
