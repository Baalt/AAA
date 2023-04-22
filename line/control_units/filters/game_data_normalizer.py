import re
from datetime import datetime


class GameDataNormalizer:
    def __init__(self, season: str, day_month: str):
        self.season = season
        self.day_month = day_month

    def convert_season_to_dmY(self):
        try:
            match = re.search('\d{2}/\d{2}', self.season)
            year_or_years = match.group().split('/')
            if len(year_or_years) == 2:
                first_half_season_year, second_half_season_year = year_or_years
                first_half_season_year = '20' + first_half_season_year
                second_half_season_year = '20' + second_half_season_year

                return self.determine_the_year_by_the_month_of_the_season(first_half_season_year=first_half_season_year,
                                                                          second_half_season_year=second_half_season_year)
        except AttributeError:
            match = re.search('\d{2}', self.season)
            if match:
                year_or_years = '20' + match.group()
                return f'{self.day_month}.{year_or_years}'

    def determine_the_year_by_the_month_of_the_season(self,
                                                      first_half_season_year: str,
                                                      second_half_season_year: str):
        try:
            if self.day_month == '29.02':
                self.day_month = '28.02'
            match_date = datetime.strptime(self.day_month, "%d.%m")

            if match_date.month in range(1, 7):
                return f'{self.day_month}.{second_half_season_year}'
            if match_date.month in range(7, 13):
                return f'{self.day_month}.{first_half_season_year}'

        except ValueError as err:
            print(f'Value Error: "{err}"')
