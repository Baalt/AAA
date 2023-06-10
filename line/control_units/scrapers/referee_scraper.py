from bs4 import BeautifulSoup


class RefereeScraper:
    def __init__(self):
        self.data = {}

    def scrape_table(self, soup: BeautifulSoup, key: str):
        table = soup.find('table', id='table')
        rows = table.find_all('tr')

        values = []
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            try:
                it1_value, it2_value = int(columns[4].text), int(columns[5].text)
                sum_value = it1_value + it2_value
                values.append(sum_value)
            except ValueError:
                continue

        self.data[key] = {
            'all': values,
            'count': len(values),
            'first_15_elements': values[:15] if len(values) >= 15 else values
        }

    def get_data(self):
        return self.data
