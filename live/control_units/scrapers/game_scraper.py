from typing import List
from bs4 import BeautifulSoup


class RealTimeGameScraper:
    keys = {
        'goals': {
            'total_text': 'Total goals',
            'team_total_text': 'Team totals goals',
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
        # Get league information from the last element with the specified class
        league_info = soup.select('.ev-header__caption--1nhETX:last-of-type')[-1].text
        self.game_info['league'] = league_info

    def scrape_team_names(self, soup: BeautifulSoup, separator=' — '):
        # Get team names
        team1_name = soup.select_one('.team1--3LWqC1 .ev-team__name--6W4ZZS').text
        team2_name = soup.select_one('.team2--4SM4BI .ev-team__name--6W4ZZS').text
        self.game_info['team1_name'] = team1_name
        self.game_info['team2_name'] = team2_name
        return f"{team1_name}{separator}{team2_name}"

    def scrape_match_time(self, soup: BeautifulSoup):
        # Get match time
        try:
            match_time = soup.select_one('.ev-live-time__timer--6XZjl4').text
            self.game_info['match_time'] = match_time
        except AttributeError:
            self.game_info['match_time'] = 'Match has not started'

    def scrape_match_score(self, soup: BeautifulSoup):
        scores: List[int] = [int(score.text) for score in soup.select('.ev-score--4dG0AR._main--1NGLZW')]
        if len(scores) == 2:
            score_str = f"{scores[0]} : {scores[1]}"
            self.game_info['match_score'] = score_str

    def scrape_red_cards(self, soup: BeautifulSoup):
        # Find the first element that matches the specified selector
        red_card_elem = soup.select_one('div.ev-comment__tail--5ILNNG._style_red--3JeHeN[title="Sending off"]')
        red_card_text = red_card_elem.text if red_card_elem else '0-0'
        self.game_info['red cards'] = red_card_text

    def scrape_match_stats(self, soup: BeautifulSoup):
        match_stats = {}
        stat_elements = soup.select('div.title--1ynOw7')
        for stat_element in stat_elements:
            stat_name = stat_element.find('span', {'class': 'caption-new--IGcNO4'}).text
            score_element = stat_element.find_next('div', {'class': 'score--6jKiQM'})
            try:
                score = score_element.text.strip()
            except AttributeError:
                score = '0:0'
            team1_score, team2_score = score.split(':')
            match_stats[stat_name] = {'team1': int(team1_score), 'team2': int(team2_score)}
        self.game_info['match_stats'] = match_stats

    def collect_stats(self, soup, match_stat, total_text, team_total_text, handicap_text):
        # Find all market-group-box elements and loop through each one
        market_boxes = soup.select('.market-group-box--z23Vvd')
        for box in market_boxes:
            # Find all text-new elements and check for Total goals
            scoring_category = box.find('div', {'class': 'text-new--2WAqa8'})
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

        for row in info_box.find_all('div', {'class': 'row-common--33mLED'}):
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
        for cell in info_box.select('div[class*="cell-wrap--LHnTwg"]'):
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
        cells = info_box.select('div[class*="cell-wrap--LHnTwg"]')
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
        divs = info_box.find_all('div', {'class': 'header-text--5VlC6H'})
        return [div.text for div in divs if div.text not in ['Over', 'Under', '']]

    def __replace_nbsp_with_space(self, lst):
        """Replace all occurrences of \xa0 character with a space in the given list of strings."""
        return [name.replace('\xa0', ' ') for name in lst]

    def __get_team_box(self, info_box, index):
        try:
            command_box = info_box.find_all(
                'div', {'class': "section--5JAm4a _horizontal--18WrKP"})[index].find_all(
                'div', {'class': "row-common--33mLED"})
        except IndexError:
            command_box = None
        return command_box
