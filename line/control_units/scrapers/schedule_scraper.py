from typing import Optional
from bs4 import BeautifulSoup

from browser.browser import SmartChromeDriver


class ScheduleScraper:
    def __init__(self, soup: Optional[BeautifulSoup] = None):
        self.schedule = {}
        if soup:
            self.scrape_schedule_data(soup)
            self.scrape_date_data(soup)

    def show_schedule_data(self):
        from pprint import pprint
        pprint(self.schedule)

    def get_schedule_data(self):
        return self.schedule

    def scrape_schedule_data(self, soup: BeautifulSoup) -> None:
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

    def scrape_date_data(self, soup: BeautifulSoup) -> None:
        date_button = soup.find('button', attrs={'class': 'datepicker-day btn btn-sm btn-light active'})
        self.schedule['date'] = date_button.find('span', attrs={'class': 'date-short'}).get_text(
            strip=True) if date_button else None


if __name__ == '__main__':
    driver = SmartChromeDriver()
    driver.maximize_window()
    driver.open_page(url='https://smart-tables.ru/')

    soup = BeautifulSoup(driver.get_page_html(), 'lxml')
    scraper = ScheduleScraper()
    scraper.scrape_date_data(soup=soup)
    scraper.scrape_schedule_data(soup=soup)
    scraper.show_schedule_data()
