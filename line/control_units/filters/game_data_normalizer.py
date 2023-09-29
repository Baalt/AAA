import re
import datetime

class GameDataNormalizer:
    def __init__(self):
        self.previous_dm = None
        self.current_year = None

    def find_current_year(self, day_month):
        if self.current_year == None:
            current_year = datetime.datetime.now().year
            self.current_year = str(current_year)[-2:]
            self.previous_dm = day_month

    def convert_season_to_dmY(self, season, day_month):
        self.find_current_year(day_month)
        if self.current_year in season:
            prev_month = int(self.previous_dm.split('.')[1])
            curr_month = int(day_month.split('.')[1])
            self.previous_dm = day_month
            if prev_month < curr_month:
                self.current_year = str(int(self.current_year) - 1)
            return f"{day_month}.20{self.current_year}"

        else:
            match = re.search(r'\((\d{2}/\d{2}|\d{4})\)', season)
            if match:
                year_pattern = match.group(1)
                self.current_year = year_pattern[-2:]
                self.previous_dm = day_month
            return f"{day_month}.20{self.current_year}"



