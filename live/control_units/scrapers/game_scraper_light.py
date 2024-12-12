from bs4 import BeautifulSoup
from pprint import pprint


class GameScraperLight:
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
            self.extract_team_names(scoreboard_div)
            self.extract_match_score(scoreboard_div)

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