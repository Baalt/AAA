from bs4 import BeautifulSoup
from pprint import pprint

from utils.stat_switcher import live_stat_dct


class GameScraperLight:
    keys = {
        'yellow cards': {
            'total_text': 'Total yellow cards',
            'handicap_text': 'Yellow cards handicap',
        },
        'fouls': {
            'total_text': 'Total fouls', }
    }

    def __init__(self):
        self.game_info = {}

    def show_game_info(self):
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
            self.extract_live_team_names(scoreboard_div)
            self.extract_match_score(scoreboard_div)
        else:
            self.game_info['match_time'] = 'Line'
            self.game_info['match_score'] = '0:0'
            self.extract_line_team_names(soup)

    def get_scoreboard_div(self, soup):
        return soup.select_one('div[class*="scoreboard__table"]')

    def extract_match_time(self, scoreboard_div):
        try:
            match_time = scoreboard_div.select_one('span[class*="scoreboard-timer__value"]').text
            self.game_info['match_time'] = match_time
        except (AttributeError, IndexError):
            self.game_info['match_time'] = 'Match has not started'

    def extract_live_team_names(self, scoreboard_div):
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

    def extract_line_team_names(self, soup):
        try:
            team1_name = soup.select_one(
                'div[class*="scoreboard-compact__main__team"][class*="team1"]').get_text(strip=True)
            self.game_info['team1_name'] = team1_name
        except (AttributeError, IndexError):
            self.game_info['team1_name'] = 'team1_not_available'

        try:
            team2_name = soup.select_one(
                'div[class*="scoreboard-compact__main__team"][class*="team2"]').get_text(strip=True)
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

    def scrape_stats(self, soup: BeautifulSoup):
        stat_set = set()
        for button in soup.select('span[class*="button"]'):
            button_text = button.get_text(strip=True)
            if button_text in live_stat_dct:
                stat_set.add(live_stat_dct[button_text])

        if not stat_set:
            stat_set.add('corners')

        self.game_info['stat_set'] = stat_set

    def extract_tournament_info(self, soup):
        rows = soup.select('div[class*="row"][class*="active"]')
        total_teams = len(soup.select('div[class*="row--jbmPK"]'))
        tournament_info = []
        for row in rows:
            try:
                rank = row.select_one('span[class*="rank"]').text.strip()
                name = row.select_one('span[class*="name"]').text.strip()
                game_played = row.select('div[class*="row_item"]')[
                    1].text.strip()
                tournament_info.append({
                    'rank': rank,
                    'name': name,
                    'game_played': game_played
                })
            except (AttributeError, IndexError):
                continue
        self.game_info['tournament_info'] = tournament_info
        self.game_info['total_teams'] = total_teams
        if self.game_info['tournament_info'] and self.game_info['total_teams']:
            return True

    def collect_stats(self, soup, match_stat, total_text, handicap_text=None):
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
