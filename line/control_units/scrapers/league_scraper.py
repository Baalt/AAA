import re

from bs4 import BeautifulSoup


class LeagueScraper:
    def __init__(self, data: dict):
        self.data = data

    def show_data(self):
        from pprint import pprint
        pprint(self.data)

    @staticmethod
    def find_all_rows(soup):
        return soup.find_all('tr', class_=re.compile(r'^(odd|even)$'))

    def scrape_league_table(self, soup: BeautifulSoup, key='goals'):
        commands_data = self.find_all_rows(soup=soup)
        team_data_list = []
        for data in commands_data:
            cells = data.find_all('td')
            team_position = cells[0].text.strip()
            team_name = cells[1].find('a').text.strip().replace('\n', '').replace('\r', '')
            games_played = cells[2].text.strip()
            avg_overall_total = cells[11 if key == 'goals' else 9].text.strip()
            avg_individual_team = cells[12 if key == 'goals' else 6].text.strip()
            avg_individual_team_against = cells[13 if key == 'goals' else 7].text.strip()
            points = cells[8].text.strip() if key == 'goals' else None
            team_data = {
                'team_position': team_position,
                'team_name': team_name,
                'games_played': games_played,
                'points': points,
                'avg_overall_total': avg_overall_total,
                'avg_individual_team': avg_individual_team,
                'avg_individual_team_against': avg_individual_team_against,
            }
            team_data_list.append(team_data)
        self.data.setdefault(key, team_data_list)


    def scrape_ref_table(self, soup: BeautifulSoup, key: str):
        ref_data_list = []
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 10:
                ref_data = {
                    'team_position': cols[0].get_text(strip=True),
                    'team_name': cols[1].get_text(strip=True),
                    'games_played': cols[2].get_text(strip=True),
                    'avg_overall_total': cols[10].get_text(strip=True)
                }
                ref_data_list.append(ref_data)
        self.data.setdefault(key, ref_data_list)