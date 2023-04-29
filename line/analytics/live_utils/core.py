import numpy as np


class BoundaryLiveValues:
    def __init__(self,
                 league: str,
                 team1_name: str,
                 team2_name: str,
                 game_number: str):
        self.main_data = {
            'league': league,
            'team1_name': team1_name,
            'team2_name': team2_name,
            'game_number': game_number
        }

    def total_calculation(self, seq: list, percent: int):
        total_under = None
        total_over = None
        for search_total in np.arange(0.5, 70.5, 1):
            win = []
            lose = []
            for real_total in seq:
                if search_total > real_total:
                    win.append(real_total)
                elif search_total < real_total:
                    lose.append(real_total)

            quantity_win = len(win)
            quantity_lose = len(lose)

            denominator = quantity_win + quantity_lose
            if denominator:
                under_percent = (quantity_win * 100) / denominator
                if under_percent >= percent:
                    total_under = search_total
                    break

        for search_total in np.arange(70.5, -0.5, -1):
            win = []
            lose = []
            for real_total in seq:
                if search_total < real_total:
                    win.append(real_total)
                elif search_total > real_total:
                    lose.append(real_total)

            quantity_win = len(win)
            quantity_lose = len(lose)

            denominator = quantity_win + quantity_lose
            if denominator:
                over_percent = (quantity_win * 100) / denominator
                if over_percent >= percent:
                    total_over = search_total
                    break

        return total_under, total_over

    def handicap_calculation(self, current_seq, opposing_seq, percent):
        if len(current_seq) == len(opposing_seq):
            for search_total in np.arange(0.5, 70.5, 1):
                win_list = []
                lose_list = []

                idx = 0
                for total in current_seq:
                    total_plus_handicap = (total + search_total) - opposing_seq[idx]
                    idx += 1

                    if total_plus_handicap > 0:
                        win_list.append(total)
                    elif total_plus_handicap < 0:
                        lose_list.append(total)

                quantity_win = len(win_list)
                quantity_lose = len(lose_list)

                denominator = quantity_win + quantity_lose
                if denominator:
                    win_percent = (quantity_win * 100) / denominator
                    if win_percent >= percent:
                        return search_total
        return None

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
