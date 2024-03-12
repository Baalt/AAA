from typing import List
from bs4 import BeautifulSoup


class RealTimeGameScraper:
    keys = {
        'goals': {
            'total_text': 'Total goals',
            'team_total_text': 'Team total goals',
            'handicap_text': 'Handicap',
        },
        'corners': {
            'total_text': 'Total corners',
            'team_total_text': 'Team totals corners',
            'handicap_text': 'Сorners handicap',
        },
        'yellow cards': {
            'total_text': 'Total yellow cards',
            'team_total_text': 'Team totals yellow cards',
            'handicap_text': 'Yellow cards handicap',
        },
        'fouls': {
            'total_text': 'Total fouls',
            'team_total_text': 'Team totals fouls',
            'handicap_text': 'Fouls handicap',
        },
        'shots on goal': {
            'total_text': 'Total shots on goal',
            'team_total_text': 'Team totals shots on goal',
            'handicap_text': 'Shots on goal handicap',
        },
        'offsides': {
            'total_text': 'Total offsides',
            'team_total_text': 'Team totals offsides',
            'handicap_text': 'Offsides handicap',
        },
        'throw-ins': {
            'total_text': 'Total throw-ins',
            'team_total_text': 'Team totals throw-ins',
            'handicap_text': 'Throw-ins handicap',
        },
        'goal kicks': {
            'total_text': 'Total goal kicks',
            'team_total_text': 'Team totals goal kicks',
            'handicap_text': 'Goal kicks handicap',
        },
    }

    def __init__(self):
        self.game_info = {'match_stats': {}}

    def show_game_info(self):
        from pprint import pprint
        pprint(self.game_info)

    def get_game_info(self):
        return self.game_info

    def scrape_league(self, soup: BeautifulSoup):
        # Find the last <a> tag within the specified div
        league_tag = soup.select('.event-view__header__caption--U2mqs a')[-1]
        # Extract the text content of the <a> tag, which should contain the league information
        league_info = league_tag.text.strip()
        print(league_info)
        self.game_info['league'] = league_info

    def scrape_team_names(self, soup: BeautifulSoup, separator=' — '):
        # Get team names
        team1_name = soup.select_one(
            '.scoreboard-compact__main__team--JipHC._team1--fKDjV .scoreboard-compact__main__team__name--LRB3V').text
        team2_name = soup.select_one(
            '.scoreboard-compact__main__team--JipHC._team2--nEcQF .scoreboard-compact__main__team__name--LRB3V').text
        self.game_info['team1_name'] = team1_name
        self.game_info['team2_name'] = team2_name
        print(f"{team1_name}{separator}{team2_name}")
        return f"{team1_name}{separator}{team2_name}"

    # def scrape_line_team_names(self, soup: BeautifulSoup, separator=' — '):
    #     # Get team names
    #     team1_name = soup.select_one('.team-statistic-1--krP2Db .ev-team__name--6W4ZZS').text
    #     team2_name = soup.select_one('.team-statistic-2--3q4zZu .ev-team__name--6W4ZZS').text
    #     self.game_info['team1_name'] = team1_name
    #     self.game_info['team2_name'] = team2_name
    #     return f"{team1_name}{separator}{team2_name}"

    def scrape_match_time(self, soup: BeautifulSoup):
        # Get match time
        try:
            match_time = soup.select_one('.scoreboard-timer__value').text
            self.game_info['match_time'] = match_time
            print(self.game_info['match_time'])
        except AttributeError:
            self.game_info['match_time'] = 'Match has not started'

    def scrape_match_score(self, soup: BeautifulSoup):
        try:
            # Find all elements with class 'column--bERXJ'
            score_columns = soup.select('.column--bERXJ')

            # Get the second occurrence of '.column--bERXJ' (index 1)
            second_score_column = score_columns[1]

            # Get the scores from the first and second columns in the second score column
            score1 = second_score_column.select_one('.column__t1--r0tu1').text
            score2 = second_score_column.select_one('.column__t2--uLoi9').text

            # Create the score string
            score_str = f"{score1} : {score2}"

            # Store the score string in game_info
            self.game_info['match_score'] = score_str
        except (AttributeError, IndexError):
            self.game_info['match_score'] = 'Scores not available'

    def scrape_red_cards(self, soup: BeautifulSoup):
        try:
            score_columns = soup.select('.column--bERXJ')
            second_score_column = score_columns[5]
            score1 = second_score_column.select_one('.column__t1--r0tu1').text
            score2 = second_score_column.select_one('.column__t2--uLoi9').text
            score_str = f"{score1} : {score2}"
            self.game_info['match_score'] = score_str
        except (AttributeError, IndexError):
            self.game_info['match_score'] = 'Scores not available'

    def scrape_yellow_cards(self, soup: BeautifulSoup):
        try:
            score_columns = soup.select('.column--bERXJ')
            second_score_column = score_columns[4]
            score1 = second_score_column.select_one('.column__t1--r0tu1').text
            score2 = second_score_column.select_one('.column__t2--uLoi9').text
            score_str = f"{score1} : {score2}"
            self.game_info['match_score'] = score_str
        except (AttributeError, IndexError):
            self.game_info['match_score'] = 'Scores not available'

    def scrape_match_stats(self, soup: BeautifulSoup):
        match_stats = {}
        stat_elements = soup.select('div.title--a22by')
        for stat_element in stat_elements:
            stat_name = stat_element.find('span', {'class': 'caption--qB8wa'}).text
            score_element = stat_element.find_next('span', {'class': 'score--rN4ok'})
            try:
                score = score_element.text.strip()
            except AttributeError:
                score = '0:0'
            team1_score, team2_score = score.split(':')
            match_stats[stat_name] = {'team1': int(team1_score), 'team2': int(team2_score)}
        self.game_info['match_stats'] = match_stats

    def collect_stats(self, soup, match_stat, total_text, team_total_text, handicap_text):
        # Find all market-group-box elements and loop through each one
        market_boxes = soup.select('.market-group-box--U9Qtj')
        for box in market_boxes:
            # Find all text-new elements and check for Total goals
            scoring_category = box.find('div', {'class': 'text--AFRgY'})
            if scoring_category:
                category = scoring_category.text
                if category == total_text:
                    self.__add_totals_info(info_box=box,
                                           match_stat=match_stat,
                                           key='totals')

                elif category == team_total_text:
                    self.__add_teams_totals_info(info_box=box,
                                                 match_stat=match_stat,
                                                 key_1='team1_totals',
                                                 key_2='team2_totals')

                elif category == handicap_text:
                    self.__add_handicaps_info(info_box=box,
                                              match_stat=match_stat,
                                              key_1='team1_handicaps',
                                              key_2='team2_handicaps')

    def __add_totals_info(self, info_box, match_stat, key):
        statistic_key_dict = []

        for row in info_box.find_all('div', {'class': 'normal-row--OHyY8'}):
            self.__extract_total_sets(row, statistic_key_dict)

        if statistic_key_dict:
            self.game_info.setdefault(match_stat, {}).update({key: statistic_key_dict})

    def __add_teams_totals_info(self, info_box, match_stat, key_1, key_2):
        statistic_dict_1, statistic_dict_2 = [], []
        try:
            command_1_box, command_2_box = self.__get_command_boxes(info_box)
        except ValueError as e:
            print('__add_teams_totals_info.__get_command_boxes(info_box) error: ', e)
            return

        if command_1_box:
            for box in command_1_box:
                self.__extract_total_sets(box, statistic_dict_1)

        if command_2_box:
            for box in command_2_box:
                self.__extract_total_sets(box, statistic_dict_2)

        if statistic_dict_1:
            self.game_info.setdefault(match_stat, {}).update({key_1: statistic_dict_1})
        if statistic_dict_2:
            self.game_info.setdefault(match_stat, {}).update({key_2: statistic_dict_2})

    def __add_handicaps_info(self, info_box, match_stat, key_1, key_2):
        statistic_dict_1, statistic_dict_2 = [], []
        try:
            command_1_box, command_2_box = self.__get_command_boxes(info_box)
        except ValueError as e:
            print('__add_handicaps_info.__get_command_boxes(info_box) error: ', e)
            return

        if command_1_box:
            for box in command_1_box:
                self.__extract_handicap_sets(box, statistic_dict_1)

        if command_2_box:
            for box in command_2_box:
                self.__extract_handicap_sets(box, statistic_dict_2)

        if statistic_dict_1:
            self.game_info.setdefault(match_stat, {}).update({key_1: statistic_dict_1})
        if statistic_dict_2:
            self.game_info.setdefault(match_stat, {}).update({key_2: statistic_dict_2})

    def __get_command_boxes(self, info_box):
        command_boxes = []
        box_team_names = self.__get_box_command_names(info_box=info_box)
        if box_team_names:
            if len(box_team_names) == 2:
                command_boxes = [self.__get_team_box(info_box, 0), self.__get_team_box(info_box, 1)]
            elif len(box_team_names) == 1:
                box_team_names = self.__replace_nbsp_with_space(lst=box_team_names)
                if self.game_info['team1_name'] == box_team_names[0]:
                    command_boxes = [self.__get_team_box(info_box, 0), None]
                elif self.game_info['team2_name'] == box_team_names[0]:
                    command_boxes = [None, self.__get_team_box(info_box, 1)]

        return command_boxes

    def __extract_total_sets(self, info_box, statistic_key_dict, total_text='Total'):
        over_under, total, over, under = None, None, None, None
        for cell in info_box.select('div[class*="cell--NEHKQ"]'):
            cell_text = cell.text.strip()
            if total_text in cell_text:
                total = cell_text.split()[-1]
                over_under = 'over'
            elif over_under == 'over':
                over = cell_text
                over_under = 'under'
            elif over_under == 'under':
                under = cell_text
                over_under = None
            if total and over and under:
                bet_set = {
                    'total_number': total,
                    'coefficient_over': over,
                    'coefficient_under': under
                }
                statistic_key_dict.append(bet_set)
                total, over, under = None, None, None

    def __extract_handicap_sets(self, info_box, statistic_key_dict, handicap_text='Hcap'):
        cells = info_box.select('div[class*="cell--NEHKQ"]')
        if len(cells) % 2 == 0:
            total, coeff = None, None
            for cell in cells:
                if handicap_text in cell.text:
                    total = cell.text.split()[-1].strip('()')
                    if total.startswith('‑'):
                        total = '-' + total.lstrip('‑')
                    elif total.startswith('+'):
                        total = total.lstrip('+')

                else:
                    coeff = cell.text.strip()

                if total != None and coeff != None:
                    coeff_set: dict = {'total_number': total,
                                       'coefficient': coeff}
                    statistic_key_dict.append(coeff_set)
                    total, coeff = None, None

    def __get_box_command_names(self, info_box):
        divs = info_box.find_all('div', {'class': 'text--dWt5e'})
        return [div.text for div in divs if div.text not in ['Over', 'Under', '']]

    def __replace_nbsp_with_space(self, lst):
        """Replace all occurrences of \xa0 character with a space in the given list of strings."""
        return [name.replace('\xa0', ' ') for name in lst]

    def __get_team_box(self, info_box, index):
        try:
            command_box = info_box.find_all(
                'div', {'class': "table--pbd8Q"})[index].find_all(
                'div', {'class': "normal-row--OHyY8"})
        except IndexError:
            command_box = None
        return command_box
