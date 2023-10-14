from bs4 import BeautifulSoup
import statistics


class RefereeScraper:
    def __init__(self):
        self.data = {}

    def scrape_table(self, soup: BeautifulSoup, key: str):
        # Extract the referee name from the HTML
        referee_name_element = soup.find('span', text=lambda text: text and "Рефери" in text)
        referee_name = referee_name_element.text if referee_name_element else ""
        try:
            self.data['referee_name']
        except KeyError:
            self.data['referee_name'] = referee_name

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

        values15 = values[:15] if len(values) >= 15 else values
        self.data[key] = {
            'all': values,
            'count': len(values),
            'first_15_elements': values15,
            'avg': round(statistics.mean(values15), 2),
        }

    def get_data(self):
        return self.data
