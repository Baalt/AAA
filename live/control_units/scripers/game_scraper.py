from bs4 import BeautifulSoup


class RealTimeGameScraper:
    def __init__(self):
        self.game_info = {'goals': {}}

    def print_game_info(self):
        from pprint import pprint
        pprint(self.game_info)

    def scrape_team_names(self, soup: BeautifulSoup):
        # Get team names
        team1_name = soup.select_one('.team1--3LWqC1 .ev-team__name--6W4ZZS').text
        team2_name = soup.select_one('.team2--4SM4BI .ev-team__name--6W4ZZS').text
        self.game_info['team1_name'] = team1_name
        self.game_info['team2_name'] = team2_name

    def scrape_match_time(self, soup: BeautifulSoup):
        # Get match time
        match_time = soup.select_one('.ev-live-time__timer--6XZjl4').text
        self.game_info['match_time'] = match_time

    def scrape_league(self, soup: BeautifulSoup):
        # Get league information from the last element with the specified class
        league_info = soup.select('.ev-header__caption--1nhETX:last-of-type')[-1].text
        self.game_info['league'] = league_info

    def collect_stats(self, soup, match_stat, total_text, team_total_text, handicap_text):
        # Find all market-group-box elements and loop through each one
        market_boxes = soup.select('.market-group-box--z23Vvd')
        for box in market_boxes:
            # Find all text-new elements and check for Total goals
            scoring_category = box.find('div', {'class': 'text-new--2WAqa8'})
            if scoring_category:
                category = scoring_category.text
                if category == total_text:
                    self.add_totals_info(info_box=box,
                                         match_stat=match_stat,
                                         key='totals')
                elif category == team_total_text:
                    self.add_teams_totals_info(info_box=box,
                                               match_stat=match_stat,
                                               key_1='team1_totals',
                                               key_2='team2_totals')
                elif category == handicap_text:
                    self.add_handicaps_info(info_box=box,
                                            match_stat=match_stat,
                                            key_1='team1_handicaps',
                                            key_2='team2_handicaps')

    def add_totals_info(self, info_box, match_stat, key):
        statistic_key_dict = []

        for row in info_box.find_all('div', {'class': 'row-common--33mLED'}):
            self.extract_total_sets(row, statistic_key_dict)

        if statistic_key_dict:
            self.game_info[match_stat].update({key: statistic_key_dict})

    def add_teams_totals_info(self, info_box, match_stat, key_1, key_2):
        statistic_dict_1, statistic_dict_2 = [], []
        command_1_box, command_2_box = self.get_command_boxes(info_box)

        if command_1_box:
            for box in command_1_box:
                self.extract_total_sets(box, statistic_dict_1)

        if command_2_box:
            for box in command_2_box:
                self.extract_total_sets(box, statistic_dict_2)

        if statistic_dict_1:
            self.game_info[match_stat].update({key_1: statistic_dict_1})
        if statistic_dict_2:
            self.game_info[match_stat].update({key_2: statistic_dict_2})

    def add_handicaps_info(self, info_box, match_stat, key_1, key_2):
        statistic_dict_1, statistic_dict_2 = [], []
        command_1_box, command_2_box = self.get_command_boxes(info_box)

        if command_1_box:
            for box in command_1_box:
                self.extract_handicap_sets(box, statistic_dict_1)

        if command_2_box:
            for box in command_2_box:
                self.extract_handicap_sets(box, statistic_dict_2)

        if statistic_dict_1:
            self.game_info[match_stat].update({key_1: statistic_dict_1})
        if statistic_dict_2:
            self.game_info[match_stat].update({key_2: statistic_dict_2})

    def get_command_boxes(self, info_box):
        command_boxes = []
        box_team_names = self.get_box_command_names(info_box=info_box)
        if box_team_names:
            if len(box_team_names) == 2:
                command_boxes = [self.get_team_box(info_box, 0), self.get_team_box(info_box, 1)]
            elif len(box_team_names) == 1:
                box_team_names = self.replace_nbsp_with_space(lst=box_team_names)
                if self.game_info['team1_name'] == box_team_names[0]:
                    command_boxes = [self.get_team_box(info_box, 0), None]
                elif self.game_info['team2_name'] == box_team_names[0]:
                    command_boxes = [None, self.get_team_box(info_box, 1)]

        return command_boxes

    def extract_total_sets(self, info_box, statistic_key_dict, total_text='Total'):
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

    def extract_handicap_sets(self, info_box, statistic_key_dict, handicap_text='Hcap'):
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
                    # total = float(total)
                    # print('handicap_total_1: ', total)

                else:
                    coeff = cell.text.strip()
                    # print('handicap_1_coeff: ', coeff)

                if total != None and coeff != None:
                    coeff_set: dict = {'total_number': total,
                                       'coefficient': coeff}
                    statistic_key_dict.append(coeff_set)
                    total, coeff = None, None

    def get_box_command_names(self, info_box):
        divs = info_box.find_all('div', {'class': 'header-text--5VlC6H'})
        return [div.text for div in divs if div.text not in ['Over', 'Under', '']]

    def replace_nbsp_with_space(self, lst):
        """Replace all occurrences of \xa0 character with a space in the given list of strings."""
        return [name.replace('\xa0', ' ') for name in lst]

    def get_team_box(self, info_box, index):
        try:
            command_box = info_box.find_all(
                'div', {'class': "section--5JAm4a _horizontal--18WrKP"})[index].find_all(
                'div', {'class': "row-common--33mLED"})
        except IndexError:
            command_box = None
        return command_box
