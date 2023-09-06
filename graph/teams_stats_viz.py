import matplotlib

matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

plt.ioff()


class TeamsStatsVisualizer:
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

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        for i in range(len(team_names)):
            alpha = 1.0
            if not team_names[i].endswith(("_1", "_2")):
                alpha = 0.6
            ax.bar(i, values[i, 0], color='black', width=0.4, alpha=alpha)

            ax.text(i, values[i, 0] + 1.5, f"{values[i, 0]} / {values[i, 1]}", ha='center', fontsize=7,
                    bbox=dict(facecolor='white', edgecolor='white', alpha=0.5, pad=1))

        ax.set_xticks(np.arange(len(team_names)))
        ax.set_xticklabels(team_names, rotation=90, fontsize=10)
        ax.set_title(f'Points - {season}')
        ax.set_xlabel('Team')
        ax.set_ylabel('Points')
        fig.tight_layout()

        fig.savefig(f"graph/data/{season}_points.png", dpi=300)
        plt.close(fig)

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
        try:
            num_bars = values.shape[1]
        except IndexError:
            print('plot_team_stats num_bars shape error')
            num_bars = ''

        colors = ['b', 'g', 'r']

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        try:
            for i in range(num_bars):
                for j, team_name in enumerate(team_names):
                    alpha = 1.0
                    if not team_name.endswith(("_1", "_2")):
                        alpha = 0.5
                    bar = ax.bar(j + i * 0.2, values[j, i], width=0.2, color=colors[i], alpha=alpha, edgecolor='white')

                    ax.text(bar.patches[0].get_x() + bar.patches[0].get_width() / 2, bar.patches[0].get_height(),
                            f"{values[j, i]:.1f}", ha='center', va='bottom', fontsize=8,
                            bbox=dict(facecolor='white', edgecolor='white', alpha=0.5, pad=1))
        except TypeError:
            pass

        ax.set_xticks(np.arange(len(team_names)))
        ax.set_xticklabels(team_names, rotation=90, fontsize=10)
        ax.set_title(f'Stats - {season}')
        ax.set_xlabel('Team')
        ax.set_ylabel(stat_key)
        fig.tight_layout()

        fig.savefig(f"graph/data/{season}_stat.png", dpi=300)
        plt.close(fig)
