from bs4 import BeautifulSoup


class ScraperMethods:
    def scrap_statistic_name(self, soup: BeautifulSoup) -> str:
        div = soup.find('div', attrs={'class': 'btn-group py-1 mr-2 stat-picker'})
        button = div.find('button', attrs={'class': 'btn btn-sm btn-light filter-button__span active'}) or div.find(
            'button', attrs={'class': 'btn btn-sm btn-light filter-button__span active has-tooltip'})
        button_name = button.get_text(strip=True)
        return button_name

    def scrap_accordion_statistic_name(self, soup: BeautifulSoup) -> str:
        current_statistic_button_name = soup.find('button', attrs={'id': "filterTypeStat"}).get_text(strip=True)
        return current_statistic_button_name

    def get_statistic_name(self, soup):
        staistic_name = self.scrap_statistic_name(soup=soup)
        if staistic_name == 'Уд. от ворот':
            staistic_name = 'Удары от ворот'
        return staistic_name


class CoefficientsScraper(ScraperMethods):

    def get_totals_data(self, soup: BeautifulSoup, coefficient_data: dict):
        # Get the statistic name
        statistic_name = self.get_statistic_name(soup=soup)
        # Find all divs containing the data
        data_divs = soup.find('div', attrs={'class': "card-body align-middle"}).find_all('div', attrs={'class': "col"})

        # Iterate over each div
        for col_num, col in enumerate(data_divs):
            # Find all tables within the div
            tables = col.find_all('table',
                                  attrs={'class': "table-sm table table-bordered matches betting-table text-center"})

            # Iterate over each table
            for table in tables:
                # Initialize lists to store the scraped data
                total_list = []
                coefficient_over_list = []
                coefficient_under_list = []

                # Find all rows within the table body
                rows = table.find('tbody').find_all('tr')

                # Iterate over each row
                for row in rows:
                    # Find all data cells within the row
                    tds = row.find_all('td')

                    # Extract the required data
                    total_number = tds[1].text.strip() if tds[1].get('class') == ['bold'] else None
                    coefficient_over = float(tds[2].text)
                    coefficient_under = float(tds[3].text)

                    # Append the data to the respective lists
                    total_list.append(total_number)
                    coefficient_over_list.append(coefficient_over)
                    coefficient_under_list.append(coefficient_under)

                # Update the coefficient_data dictionary
                if statistic_name not in coefficient_data:
                    coefficient_data[statistic_name] = {'total&coefficient': []}

                if not col_num:
                    coefficient_data[statistic_name]['total&coefficient'].append(
                        {'total_number': total_list[0],
                         'coefficient_under': max(coefficient_under_list),
                         'coefficient_over': max(coefficient_over_list)})
                else:
                    total_key = f'total_{col_num}_&coefficient'
                    if total_key not in coefficient_data[statistic_name]:
                        coefficient_data[statistic_name][total_key] = []

                    coefficient_data[statistic_name][total_key].append(
                        {'total_number': total_list[0],
                         'coefficient_under': max(coefficient_under_list),
                         'coefficient_over': max(coefficient_over_list)})

    def get_handicap_data(self, soup: BeautifulSoup, coefficient_data: dict):
        # Get the statistic name
        statistic_name = self.get_statistic_name(soup=soup)

        # Find all divs containing the data
        data_divs = soup.find('div', attrs={'class': "card-body align-middle"}).find_all('div', attrs={'class': "col"})

        # Iterate over each div
        for col_num, col in enumerate(data_divs, start=1):
            # Temporary dictionary to store the highest coefficients for each total number
            temp_dict = {}
            # Find all tables within the div
            tables = col.find_all('table',
                                  attrs={'class': "table-sm table table-bordered matches betting-table text-center"})

            # Iterate over each table
            for table in tables:
                # Find all rows within the table body
                rows = table.find_all('tbody')

                # Iterate over each row
                for row in rows:
                    # Find all data cells within the row
                    tds = row.find_all('td')

                    # Extract the required data
                    total_number = tds[0].text
                    coefficient = float(tds[1].find('span').text)

                    # Save total number and coefficient in temp dict if it's not there or if the new coefficient is higher
                    if total_number not in temp_dict or coefficient > temp_dict[total_number]:
                        temp_dict[total_number] = coefficient

            # For each column
            if statistic_name not in coefficient_data:
                coefficient_data[statistic_name] = {}

            handicap_key = f'handicap_{col_num}_&coefficient'
            if handicap_key not in coefficient_data[statistic_name]:
                coefficient_data[statistic_name][handicap_key] = []

            # Save each unique total_number with the bigger coefficient
            for total_number, coefficient in temp_dict.items():
                coefficient_data[statistic_name][handicap_key].append(
                    {'total_number': total_number, 'coefficient': coefficient})
