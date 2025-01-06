from typing import Optional
from bs4 import BeautifulSoup


class SmartScheduleScraper:
    def __init__(self, soup: Optional[BeautifulSoup] = None):
        self.schedule = {}
        if soup:
            self.scrape_schedule(soup)
            self.scrape_date(soup)

    def show_schedule_data(self):
        from pprint import pprint
        pprint(self.schedule)

    def get_schedule_data(self):
        return self.schedule

    def scrape_schedule(self, soup: BeautifulSoup) -> None:
        table_rows = soup.find('table').find_all('tr')
        league_name = None  # Initialize league_name to None
        for row in table_rows:
            try:
                league_name = row.find('a', attrs={'class': 'league-link'}).get_text(strip=True)
                league_url = row.find('a', attrs={'class': 'league-link'})['href']
                self.schedule[league_name] = {'league_url': league_url, 'match_data': []}
            except (AttributeError, TypeError):
                pass

            # Собираем данные для match_url
            try:
                match_url = \
                row.find('td', attrs={'class': 'text-right align-middle upcoming-match-prematch'}).find('a')['href']
            except (AttributeError, TypeError):
                pass

            # Собираем данные для рефери
            try:
                referee_div = row.find('div', class_='matches__referee')
                if referee_div:
                    ref_name = referee_div.find('a').get_text(strip=True)
            except (AttributeError, TypeError):
                pass

            # Собираем имена команд
            try:
                team_links = row.find_all('a', href=lambda href: href and 'team' in href)
                if len(team_links) > 1:
                    team1_name = team_links[0].get_text(strip=True)
                    team2_name = team_links[1].get_text(strip=True)
            except (AttributeError, TypeError):
                pass

            # Если собрали все данные, добавляем их в словарь
            if league_name and 'team1_name' in locals() and 'team2_name' in locals():
                self.schedule[league_name]['match_data'].append({
                    'match_url': match_url if 'match_url' in locals() else None,
                    'ref_name': ref_name if 'ref_name' in locals() else None,
                    'team1_name': team1_name,
                    'team2_name': team2_name
                })

    def scrape_date(self, soup: BeautifulSoup) -> None:
        date_button = soup.find('button', attrs={'class': 'datepicker-day btn btn-sm btn-light active'})
        self.schedule['date'] = date_button.find('span', attrs={'class': 'date-short'}).get_text(
            strip=True) if date_button else None
