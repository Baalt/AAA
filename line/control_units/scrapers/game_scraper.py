from bs4 import BeautifulSoup
from line.control_units.filters.game_data_normalizer import GameDataNormalizer


class GameScraper:
    def __init__(self, all_match_data: dict):
        self.all_match_data: dict = all_match_data

    def __str__(self) -> str:
        return '{}'.format(self.all_match_data)

    @property
    def match_data(self):
        return self.all_match_data

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

    def scrap_commands_name(self, soup: BeautifulSoup):
        self.home_command_name = soup.find_all('div',
                                               attrs={'class': "media-body"})[0].find('h5').get_text(strip=True)
        self.away_command_name = soup.find_all('div',
                                               attrs={'class': "media-body"})[1].find('h5').get_text(strip=True)

        self.all_match_data['home_command_name'] = self.home_command_name.strip('()')
        self.all_match_data['away_command_name'] = self.away_command_name.strip('()')

    def scrap_match_table_data(self, soup, tooltip=False):

        home_table = soup.find_all('table',
                                   id='table')[0].find('tbody').find_all('tr',
                                                                         attrs={'class': "match-row"})
        away_table = soup.find_all('table',
                                   id='table')[1].find('tbody').find_all('tr',
                                                                         attrs={'class': "match-row"})

        self.statistic_name = self.scrap_statistic_name(soup=soup, tooltip=tooltip)
        self.all_match_data[self.statistic_name] = {'home_collections': list(), 'away_collections': list()}
        self.dmy = GameDataNormalizer()
        [self.scrap_them_collect_to_global_storage(row, 'home_collections') for row in home_table]
        self.dmy = GameDataNormalizer()
        [self.scrap_them_collect_to_global_storage(row, 'away_collections') for row in away_table]

    def scrap_accordion_table_data(self, soup):
        home_table = soup.find_all('table',
                                   id='table')[0].find('tbody').find_all('tr',
                                                                         attrs={'class': "match-row"})
        away_table = soup.find_all('table',
                                   id='table')[1].find('tbody').find_all('tr',
                                                                         attrs={'class': "match-row"})

        self.statistic_name = self.scrap_accordion_statistic_name(soup=soup)
        self.all_match_data[self.statistic_name] = {'home_collections': list(), 'away_collections': list()}

        [self.scrap_them_collect_to_global_storage(row, 'home_collections') for row in home_table]
        [self.scrap_them_collect_to_global_storage(row, 'away_collections') for row in away_table]

    def scrap_them_collect_to_global_storage(self, row: BeautifulSoup, home_away_key: str):
        season = row.find_all('td')[1].find('a').get_text(strip=True)
        day_month = row.find_all('td')[2].get_text(strip=True)
        dmY = self.dmy.convert_season_to_dmY(season=season, day_month=day_month)
        home_command = row.find_all('td')[3].find('a').get_text(strip=True)
        away_command = row.find_all('td')[6].find('a').get_text(strip=True)

        home_command_individual_total = row.find_all('td')[4].get_text(strip=True)
        away_command_individual_total = row.find_all('td')[5].get_text(strip=True)

        if home_command_individual_total != '?' and away_command_individual_total != '?':
            data_collect = {'dmY': dmY,
                            'home_command': home_command,
                            'away_command': away_command,
                            'home_command_individual_total': home_command_individual_total,
                            'away_command_individual_total': away_command_individual_total}

            self.all_match_data[self.statistic_name][home_away_key].append(data_collect)

    def get_name_and_count_of_games_with_last_trainer(self, soup: BeautifulSoup):
        home_table = soup.find_all('table',
                                   id='table')[0].find('tbody').find_all('tr')
        away_table = soup.find_all('table',
                                   id='table')[1].find('tbody').find_all('tr')

        def add_trainer_date(table, home_away_trainer_key: str):
            n = 0
            for tr in table:
                if len(tr) == 21:
                    n += 1
                elif len(tr) == 1:
                    text: str = tr.get_text(strip=True)
                    if text.startswith('❗'):
                        self.all_match_data[home_away_trainer_key] = {
                            f'count_games_with_command_{home_away_trainer_key}': n,
                            'trainer_name': text}
                        break

            try:
                self.all_match_data[home_away_trainer_key]
            except KeyError:
                self.all_match_data[home_away_trainer_key] = {'count_games_with_command': n,
                                                              'trainer_name': f'Maybe trainer not changed for {n} games'
                                                                              ' clarify information'}

        add_trainer_date(table=home_table, home_away_trainer_key='home_trainer')
        add_trainer_date(table=away_table, home_away_trainer_key='away_trainer')
