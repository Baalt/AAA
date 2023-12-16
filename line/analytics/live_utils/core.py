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
        self.league = league
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.game_number = game_number
        try:
            if self.referee_data:
                self.referee_name = self.referee_data['referee_name']
            else:
                self.referee_name = None
        except KeyError:
            self.referee_name = None

        self.main_data = {
            'check': None,
            'league': self.league,
            'team1_name': self.team1_name,
            'team2_name': self.team2_name,
            'game_number': self.game_number,
            'big_matrix_data': self.big_matrix_data,
            'year_matrix_data': self.year_matrix_data,
            'referee_name': self.referee_name,
            'yellow cards_reff_15_over': None,
            'yellow cards_reff_15_under': None,
            'yellow cards_reff_all_over': None,
            'yellow cards_reff_all_under': None,
            'fouls_reff_15_over': None,
            'fouls_reff_15_under': None,
            'fouls_reff_all_over': None,
            'fouls_reff_all_under': None
        }

    def total_calculation(self, seq: list, percent: int):
        total_under = None
        total_over = None
        try:
            total_count = len(seq)
        except TypeError:
            return None, None


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

                try:
                    total_count = len(current_seq)
                except TypeError:
                    return None

                percent_current_seq_greater = round((quantity_win / total_count) * 100, 2)
                if percent_current_seq_greater >= percent:
                    return search_total

    def over_under_define(self, seq: list, over_under: str):
        if seq:
            if over_under == 'under':
                return max(seq)
            elif over_under == 'over':
                return min(seq)

    def handicap_define(self, seq: list):
        if seq:
            return max(seq)
