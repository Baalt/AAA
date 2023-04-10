import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
plt.ioff()


class MatchStatsVisualizer:
    def __init__(self, data):
        self.data = data
        self.sorted_keys = ['Fouls', 'Yellow cards', 'Throw-ins', 'Offsides', 'Goal kicks', 'Shots on goal', 'Corners']
        self.category_indices = {category: index for index, category in enumerate(self.sorted_keys)}

    def plot_bar_chart(self):
        categories = list(self.data.keys())
        categories_not_sorted = [cat for cat in categories if cat not in self.sorted_keys]
        categories_sorted = sorted([cat for cat in categories if cat in self.sorted_keys],
                                   key=lambda x: self.category_indices.get(x))
        categories = categories_not_sorted + categories_sorted

        team1_data = []
        team2_data = []
        for cat in categories:
            if 'team1' in self.data[cat]:
                team1_data.append(int(self.data[cat]['team1']))
            else:
                team1_data.append(0)
            if 'team2' in self.data[cat]:
                team2_data.append(int(self.data[cat]['team2']))
            else:
                team2_data.append(0)
        y = range(len(categories))

        fig, ax = plt.subplots()
        for i, (team1_val, team2_val) in enumerate(zip(team1_data, team2_data)):
            if team1_val > team2_val:
                team1_color = 'green'
                team2_color = 'red'
            elif team2_val > team1_val:
                team1_color = 'red'
                team2_color = 'green'
            else:
                team1_color = 'gray'
                team2_color = 'gray'

            ax.barh(i, -team1_val, height=0.3, label='Team 1', color=team1_color)
            ax.barh(i, team2_val, height=0.3, label='Team 2', color=team2_color)

            # Add bar labels above each bar with a white frame
            if team1_val > 0:
                ax.text(-team1_val - max(team1_data) * 0.05, i, str(team1_val), ha='right', va='center', color='black',
                        fontsize=10,
                        bbox=dict(facecolor=team1_color, edgecolor='none', alpha=1, pad=3))
            if team2_val > 0:
                ax.text(team2_val + max(team2_data) * 0.05, i, str(team2_val), ha='left', va='center', color='black',
                        fontsize=10,
                        bbox=dict(facecolor=team2_color, edgecolor='none', alpha=1, pad=3))

        ax.set_yticks(y)
        ax.set_yticklabels(categories, fontsize=12)
        ax.set_title('Match Statistics', fontsize=16)

        max_count = max(max(team1_data), max(team2_data)) + 1
        ax.set_xlim(-max_count, max_count)
        ax.set_xticks([0])
        ax.set_xticklabels([0])

        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_color('none')  # remove x-axis strip

        ax.spines['top'].set_color('none')

        ax.xaxis.labelpad = max_count * 2
        ax.yaxis.labelpad = 20

        # Save the graph as an image
        plt.savefig(f"graph/data/live_stats.png")
