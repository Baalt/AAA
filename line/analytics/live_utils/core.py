from collections import Counter
import numpy as np


class BoundaryLiveValues:
    def __init__(self,
                 league: str,
                 team1_name: str,
                 team2_name: str,
                 game_number: str,
                 referee_data: dict,
                 big_matrix_data,
                 year_matrix_data,
                 ):

        self.big_matrix_data = big_matrix_data,
        self.year_matrix_data = year_matrix_data
        self.referee_data = referee_data

        try:
            if self.referee_data:
                referee_name = self.referee_data['referee_name']
            else:
                referee_name = None
        except KeyError:
            referee_name = None

        self.main_data = {
            'league': league,
            'team1_name': team1_name,
            'team2_name': team2_name,
            'game_number': game_number,
            'big_matrix_data': self.big_matrix_data,
            'year_matrix_data': self.year_matrix_data,
            'referee_name': referee_name,
        }

    def total_calculation(self, seq: list, percent: int):
        total_under = None
        total_over = None
        total_count = len(seq)

        # Calculation for totals under a certain threshold
        if total_count:
            for search_total in np.arange(0.5, 70.5, 1):
                win_counter = Counter()

                for real_total in seq:
                    if search_total > real_total:
                        win_counter[real_total] += 1

                quantity_win = sum(win_counter.values())

                under_percent = round((quantity_win / total_count) * 100, 2)

                if under_percent >= percent:
                    total_under = search_total
                    break

            # Calculation for totals over a certain threshold
            for search_total in np.arange(70.5, -0.5, -1):
                win_counter = Counter()

                for real_total in seq:
                    if search_total < real_total:
                        win_counter[real_total] += 1

                quantity_win = sum(win_counter.values())

                over_percent = round((quantity_win / total_count) * 100, 2)

                if over_percent >= percent:
                    total_over = search_total
                    break

        return total_under, total_over

    def handicap_calculation(self, current_seq, opposing_seq, percent):
        if current_seq and (len(current_seq) == len(opposing_seq)):
            for search_total in np.arange(0.5, 70.5, 1):
                win_counter = Counter()

                idx = 0
                for total in current_seq:
                    total_plus_handicap = (total + search_total) - opposing_seq[idx]
                    idx += 1

                    if total_plus_handicap > 0:
                        win_counter[total] += 1

                quantity_win = sum(win_counter.values())

                total_count = len(current_seq)
                percent_current_seq_greater = round((quantity_win / total_count) * 100, 2)
                if percent_current_seq_greater >= percent:
                    return search_total

    def over_under_define(self, seq: list, over_under: str):
        for _ in seq:
            if _ is None:
                return None
        if over_under == 'under':
            return max(seq)
        if over_under == 'over':
            return min(seq)

    def handicap_define(self, seq: list):
        for _ in seq:
            if _ is None:
                return None
        return max(seq)
