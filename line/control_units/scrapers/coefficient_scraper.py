from bs4 import BeautifulSoup


class ScraperMethods:
    def scrap_statistic_name(self, soup: BeautifulSoup, tooltip=False) -> str:
        button_class = 'btn btn-sm btn-light active'
        if tooltip:
            button_class = button_class + ' has-tooltip'

        current_statistic_button_name = soup.find(
            'button', attrs={'class': button_class}
        ).get_text(strip=True)

        return current_statistic_button_name

    def scrap_accordion_statistic_name(self, soup: BeautifulSoup) -> str:
        current_statistic_button_name = soup.find('button', attrs={'id': "filterTypeStat"}).get_text(strip=True)
        return current_statistic_button_name

    def get_statistic_name(self, soup, tooltip):
        staistic_name = self.scrap_statistic_name(soup=soup, tooltip=tooltip)
        if staistic_name == 'Уд. от ворот':
            staistic_name = 'Удары от ворот'
        return staistic_name


class CoefficientsScraper(ScraperMethods):
    def get_totals_data(self, soup: BeautifulSoup, coefficient_data: dict, tooltip=False):
        data = soup.find_all('table',
                             attrs={'class': "table-sm table table-bordered matches betting-table text-center"})
        for row in data:
            row = row.get_text().split('%')
            for each_data in row:
                coefficient_data_row_list = each_data.split()
                if len(coefficient_data_row_list) == 9:
                    total_number = coefficient_data_row_list[5]
                    coefficient_over = coefficient_data_row_list[-3]
                    coefficient_under = coefficient_data_row_list[-2]
                    statistic_name = self.get_statistic_name(soup=soup, tooltip=tooltip)
                    if statistic_name not in coefficient_data:
                        coefficient_data[statistic_name] = {'total&coefficient': []}
                    coefficient_data[statistic_name]['total&coefficient'].append(
                        {'total_number': total_number,
                         'coefficient_under': coefficient_under,
                         'coefficient_over': coefficient_over})

                elif len(coefficient_data_row_list) == 11:
                    home_or_away_number = coefficient_data_row_list[2]
                    total_number = coefficient_data_row_list[-4]
                    coefficient_over = coefficient_data_row_list[-3]
                    coefficient_under = coefficient_data_row_list[-2]

                    statistic_name = self.get_statistic_name(soup=soup, tooltip=tooltip)
                    if f'total_{home_or_away_number}_&coefficient' not in coefficient_data[statistic_name]:
                        coefficient_data[statistic_name][f'total_{home_or_away_number}_&coefficient'] = []
                    coefficient_data[statistic_name][f'total_{home_or_away_number}_&coefficient'].append(
                        {'total_number': total_number,
                         'coefficient_under': coefficient_under,
                         'coefficient_over': coefficient_over})


    def get_handicap_data(self, soup: BeautifulSoup, coefficient_data: dict, tooltip=False):
        data = soup.find_all('table',
                             attrs={'class': "table-sm table table-bordered matches betting-table text-center"})
        for row in data:
            row_text: str = row.get_text().strip()
            if row_text.startswith('Фора'):
                row_list = row_text.split()
                total_number = None
                statistic_name = self.get_statistic_name(soup=soup, tooltip=tooltip)
                if statistic_name not in coefficient_data:
                    coefficient_data[statistic_name] = {}
                for n in range(3, len(row_list)):
                    if n % 2:
                        total_number = row_list[n]
                    else:
                        if total_number:
                            if f'handicap_{row_list[1]}_&coefficient' not in coefficient_data[statistic_name]:
                                coefficient_data[statistic_name][f'handicap_{row_list[1]}_&coefficient'] = []
                            coefficient_data[statistic_name][f'handicap_{row_list[1]}_&coefficient'].append(
                                {'total_number': total_number, 'coefficient': row_list[n]})
