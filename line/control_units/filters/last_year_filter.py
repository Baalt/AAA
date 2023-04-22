from datetime import datetime
from dateutil.relativedelta import relativedelta


class LastYearFilter:
    def __init__(self, all_match_data: dict, all_referee_data: dict = None):
        self.all_match_data = all_match_data
        self.all_referee_data = all_referee_data
        self.today_minus_one_year = datetime.now() - relativedelta(years=1)

    def filter_home_away_collections(self, home_away_key: str):
        for statistic_name in self.all_match_data:
            if not statistic_name.startswith('home') and not statistic_name.startswith('away'):
                copy_list_of_matches = self.all_match_data[statistic_name][home_away_key].copy()
                for match in copy_list_of_matches:
                    try:
                        dmY = match['dmY']
                        if dmY is None:
                            self.all_match_data[statistic_name][home_away_key].pop(
                                self.all_match_data[statistic_name][home_away_key].index(match))

                        elif len(dmY) == 10 and '.' in dmY:
                            match_date_object = datetime.strptime(dmY, '%d.%m.%Y')
                            if self.today_minus_one_year > match_date_object:
                                self.all_match_data[statistic_name][home_away_key].pop(
                                    self.all_match_data[statistic_name][home_away_key].index(match))

                    except KeyError as err:
                        print('Key Error: ', err)

                    except Exception as err:
                        print('unexpected Error:', err)

    def filter_referee_collections(self):
        if self.all_referee_data:
            for statistic_name in self.all_referee_data:
                if isinstance(self.all_referee_data[statistic_name], list):
                    copy_list_of_matches = self.all_referee_data[statistic_name].copy()
                    for match in copy_list_of_matches:
                        try:
                            dmY = match['dmY']
                            if dmY is None:
                                self.all_referee_data[statistic_name].pop(
                                    self.all_referee_data[statistic_name].index(match))

                            elif len(dmY) == 10 and '.' in dmY:
                                match_date_object = datetime.strptime(dmY, '%d.%m.%Y')
                                if self.today_minus_one_year > match_date_object:
                                    self.all_referee_data[statistic_name].pop(
                                        self.all_referee_data[statistic_name].index(match))

                        except KeyError as err:
                            print('Key Error: ', err)

                        except Exception as err:
                            print('unexpected Error:', err)
