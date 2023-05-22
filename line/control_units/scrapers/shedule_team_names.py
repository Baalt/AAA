from bs4 import BeautifulSoup

class CommandNamesScraper:
    def __init__(self):
        self.teams = []

    def scrape(self, soup: BeautifulSoup):
        tbodies = soup.find_all('tbody')
        for tbody in tbodies:
            rows = tbody.find_all('tr', {'class': 'd-none d-md-table-row', 'data-v-40454e05': True})
            for row in rows:
                team_anchors = row.find_all('a', {'class': ''})
                if len(team_anchors) == 2:
                    team_one = team_anchors[0].text.strip()
                    team_two = team_anchors[1].text.strip()
                    self.teams.append({'team1': team_one, 'team2': team_two})
        return self.teams
