from bs4 import BeautifulSoup


class RealTimeGameScraper:
    keys = {
        'yellow cards': {
            'total_text': 'Total yellow cards',
        },
        'fouls': {
            'total_text': 'Total fouls', }
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
        league_tag = soup.select('div[class*="caption__left"] a')[-1]
        # Extract the text content of the <a> tag, which should contain the league information
        league_info = league_tag.text.strip()
        self.game_info['league'] = league_info

    def scrape_game_info(self, soup: BeautifulSoup):
        scoreboard_div = self.get_scoreboard_div(soup)
        if scoreboard_div:
            self.extract_match_time(scoreboard_div)
            self.extract_team_names(scoreboard_div)
            self.extract_match_score(scoreboard_div)
            self.extract_card_scores(scoreboard_div, 'yellow')
            self.extract_card_scores(scoreboard_div, 'red')

    def get_scoreboard_div(self, soup):
        return soup.select_one('div[class*="scoreboard__table"]')

    def extract_match_time(self, scoreboard_div):
        try:
            match_time = scoreboard_div.select_one('span[class*="scoreboard-timer__value"]').text
            self.game_info['match_time'] = match_time
        except (AttributeError, IndexError):
            self.game_info['match_time'] = 'Match has not started'

    def extract_team_names(self, scoreboard_div):
        try:
            team1_name = scoreboard_div.select_one('div[class*="column__t1"]').get_text(strip=True)
            self.game_info['team1_name'] = team1_name
        except (AttributeError, IndexError):
            self.game_info['team1_name'] = 'team1_not_available'

        try:
            team2_name = scoreboard_div.select_one('div[class*="column__t2"]').get_text(strip=True)
            self.game_info['team2_name'] = team2_name
        except (AttributeError, IndexError):
            self.game_info['team2_name'] = 'team2_not_available'

    def extract_match_score(self, scoreboard_div):
        try:
            active_score = scoreboard_div.select('div[class*="active"]')[-1]
            score1 = active_score.select_one('div[class*="column__t1"]').text
            score2 = active_score.select_one('div[class*="column__t2"]').text
            score_str = f"{score1} : {score2}"
            self.game_info['match_score'] = score_str
        except (AttributeError, IndexError):
            self.game_info['match_score'] = 'Scores not available'

    def extract_card_scores(self, scoreboard_div, card_color):
        card_key = f'{card_color}_score'
        card_found = False
        card_divs = scoreboard_div.select('div[class*="column--fgNW"]')
        for d in card_divs:
            if card_found:
                break
            svg = d.select_one(f'svg[class*="{card_color}"]')
            if svg:
                try:
                    score1 = d.select_one('div[class*="column__t1"]').text
                    score2 = d.select_one('div[class*="column__t2"]').text
                    score_str = f"{score1} : {score2}"
                    self.game_info[card_key] = score_str
                    card_found = True  # Stop checking further once a card is found
                except (AttributeError, IndexError):
                    self.game_info[card_key] = f'{card_color.capitalize()} score not available'
            else:
                if card_key not in self.game_info:
                    self.game_info[card_key] = f'{card_color.capitalize()} card not found'

    def scrape_match_stats(self, soup: BeautifulSoup):
        match_stats = {}
        stat_elements = soup.select('div.title--npxIh')
        for stat_element in stat_elements:
            stat_name = stat_element.find('span', {'class': 'caption--Xh07e'}).text
            score_element = stat_element.find_next('span', {'class': 'score--PtMoO'})
            try:
                score = score_element.text.strip()
            except AttributeError:
                score = '0:0'
            team1_score, team2_score = score.split(':')
            match_stats[stat_name] = {'team1': int(team1_score), 'team2': int(team2_score)}
        self.game_info['match_stats'] = match_stats

    def collect_stats(self, soup, match_stat, total_text):
        # Find all market-group-box elements and loop through each one
        market_boxes = soup.select('div[class*=market-group-box]')
        for box in market_boxes:
            # Find all text-new elements and check for Total goals
            scoring_category = box.select_one('div[class*=text]')
            if scoring_category:
                category = scoring_category.text
                if category == total_text:
                    self.__add_totals_info(info_box=box,
                                           match_stat=match_stat,
                                           key='totals')

    def __add_totals_info(self, info_box, match_stat, key):
        statistic_key_dict = []

        for row in info_box.select('div[class*=normal-row]'):
            self.__extract_total_sets(row, statistic_key_dict)

        if statistic_key_dict:
            self.game_info.setdefault(match_stat, {}).update({key: statistic_key_dict})

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
