from collections import Counter

import numpy as np


class StatMath:
    def search_under_total(self, seq: list, percent: int = 93):
        total_under = None
        try:
            total_count = len(seq)
        except TypeError:
            return None

        # Calculation for totals under a certain threshold
        if total_count:
            for search_total in np.arange(0.5, 60.5, 1):
                win_counter = Counter()

                for real_total in seq:
                    if search_total > real_total:
                        win_counter[real_total] += 1

                quantity_win = sum(win_counter.values())

                under_percent = round((quantity_win / total_count) * 100, 2)

                if under_percent >= percent:
                    total_under = search_total
                    break

        return total_under

    def search_over_total(self, seq: list, percent: int = 93):
        total_over = None
        try:
            total_count = len(seq)
        except TypeError:
            return None

        # Calculation for totals under a certain threshold
        if total_count:
            # Calculation for totals over a certain threshold
            for search_total in np.arange(60.5, -0.5, -1):
                win_counter = Counter()

                for real_total in seq:
                    if search_total < real_total:
                        win_counter[real_total] += 1

                quantity_win = sum(win_counter.values())

                over_percent = round((quantity_win / total_count) * 100, 2)

                if over_percent >= percent:
                    total_over = search_total
                    break

        return total_over

    def calculate_percent_by_total(self, seq: list, total: float):
        if not seq:
            return None, None

        less_than_total = 0
        greater_than_total = 0

        for number in seq:
            if number < total:
                less_than_total += 1
            elif number > total:
                greater_than_total += 1

        total_count = len(seq)
        less_than_percentage = round((less_than_total / total_count) * 100, 2)
        greater_than_percentage = round((greater_than_total / total_count) * 100, 2)

        return less_than_percentage, greater_than_percentage
