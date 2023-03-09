from bs4 import BeautifulSoup


class RealTimeGameScraper:
    def __init__(self):
        self.game_info = {'goals': {}}

    def print_game_info(self):
        from pprint import pprint
        pprint(self.game_info)

    def scrape_team_names(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Get team names
        team1_name = soup.select_one('.team1--3LWqC1 .ev-team__name--6W4ZZS').text
        team2_name = soup.select_one('.team2--4SM4BI .ev-team__name--6W4ZZS').text
        self.game_info['team1_name'] = team1_name
        self.game_info['team2_name'] = team2_name

    def scrape_match_time(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Get match time
        match_time = soup.select_one('.ev-live-time__timer--6XZjl4').text
        self.game_info['match_time'] = match_time

    def scrape_league(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Get league information from the last element with the specified class
        league_info = soup.select('.ev-header__caption--1nhETX:last-of-type')[-1].text
        self.game_info['league'] = league_info

    def collect_stats(self, html, match_stats, total_text='Total', team_total_text='Team', handicap_text='Handicap'):
        soup = BeautifulSoup(html, 'lxml')

        # Find all market-group-box elements and loop through each one
        market_boxes = soup.select('.market-group-box--z23Vvd')
        for box in market_boxes:
            # Find all text-new elements and check for Total goals
            scoring_category = box.find('div', {'class': 'text-new--2WAqa8'})
            if scoring_category:
                if scoring_category.text.startswith(total_text):
                    self.add_total_and_odds(info_box=box,
                                            match_stats=match_stats,
                                            key='totals')
                elif scoring_category.text.startswith(team_total_text):
                    self.add_teams_totals_and_odds(info_box=box,
                                                   match_stats=match_stats,
                                                   key_1='team1_totals',
                                                   key_2='team2_totals')
                elif scoring_category.text.startswith(handicap_text):
                    pass

    def add_total_and_odds(self, info_box, match_stats, key):
        statistic_key_dict = []

        for row in info_box.find_all('div', {'class': 'row-common--33mLED'}):
            self.extract_coefficient_sets(row, statistic_key_dict)

        if statistic_key_dict:
            self.game_info[match_stats].update({key: statistic_key_dict})

    def add_teams_totals_and_odds(self, info_box, match_stats, key_1, key_2):
        statistic_key1_dict, statistic_key2_dict = [], []
        command_1_box, command_2_box = None, None
        box_team_names = self.get_box_command_names(info_box=info_box)
        if box_team_names:
            if len(box_team_names) == 2:
                command_1_box = self.get_team_box(info_box, 0)
                command_2_box = self.get_team_box(info_box, 1)
            elif len(box_team_names) == 1:
                box_team_names = self.replace_nbsp_with_space(lst=box_team_names)
                if self.game_info['team1_name'] == box_team_names[0]:
                    command_1_box = self.get_team_box(info_box, 0)
                    command_2_box = None
                elif self.game_info['team2_name'] == box_team_names[0]:
                    command_1_box = None
                    command_2_box = self.get_team_box(info_box, 1)

            if command_1_box:
                for box in command_1_box:
                    self.extract_coefficient_sets(box, statistic_key1_dict)

            if command_2_box:
                for box in command_2_box:
                    self.extract_coefficient_sets(box, statistic_key2_dict)

        if statistic_key1_dict:
            self.game_info[match_stats].update({key_1: statistic_key1_dict})
        if statistic_key2_dict:
            self.game_info[match_stats].update({key_2: statistic_key2_dict})

    def extract_coefficient_sets(self, info_box, statistic_key_dict, total_text='Total'):
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

    def get_box_command_names(self, info_box):
        divs = info_box.find_all('div', {'class': 'header-text--5VlC6H'})
        return [div.text for div in divs if div.text not in ['Over', 'Under']]

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
