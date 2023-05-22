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
                self.schedule[league_name] = {'league_url': league_url, 'match_url': []}
            except (AttributeError, TypeError):
                pass

            try:
                match_url = \
                    row.find('td', attrs={'class': 'text-right align-middle upcoming-match-prematch'}).find('a')['href']
                self.schedule[league_name]['match_url'].append(match_url)
            except (AttributeError, TypeError):
                pass

    def scrape_date(self, soup: BeautifulSoup) -> None:
        date_button = soup.find('button', attrs={'class': 'datepicker-day btn btn-sm btn-light active'})
        self.schedule['date'] = date_button.find('span', attrs={'class': 'date-short'}).get_text(
            strip=True) if date_button else None
