import time

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser.browser import LiveChromeDriver
from line.control_units.scrapers.game_scraper import GameScraper


class GameCollector:
    def __init__(self, driver: LiveChromeDriver, league: str):
        self.driver = driver
        self.league = league
        self.all_match_data = {}

        self.scraper = GameScraper(all_match_data=self.all_match_data)
        # buttons
        self.quantity_of_matches_input, \
            self.quantity_of_matches_fix_input_clicker = self.driver.buttons.quantity_of_matches_buttons
        try:
            self.season_home_button_all, \
                self.season_away_button_all = self.driver.buttons.teams_season_buttons_all
        except NoSuchElementException:
            raise AttributeError

        try:
            self.current_league_home_command_button, \
                self.current_league_away_command_button = self.driver.buttons.current_league_command_buttons(
                league=self.league)
        except AttributeError:
            print('GameCollectorError address: line/control_units/managers/games_collector/GameCollector.__init__(...)'
                  'current_league_home_command_button, current_league_away_command_button NOT FOUND!!!')
            raise AttributeError

    @property
    def get_data(self):
        return self.all_match_data

    def filter_out(self, number_of_matches=100):
        self.quantity_of_matches_input.clear()
        self.quantity_of_matches_input.send_keys(number_of_matches)
        self.quantity_of_matches_fix_input_clicker.click()

        self.season_home_button_all.click()
        self.season_away_button_all.click()

        self.current_league_home_command_button.click()
        self.current_league_away_command_button.click()

        self.driver.buttons.get_refresh_button().click()
        time.sleep(1)

    def scrap_accordion_data(self):
        self.driver.buttons.get_other_button().click()
        self.driver.buttons.get_drop_down_button(button_text='Удары от ворот').click()
        self.refresh_page()
        time.sleep(1)

        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.scrap_accordion_table_data(soup=soup)

    def get_match_data(self):
        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
        self.scraper.scrap_commands_name(soup)
        try:
            self.scraper.get_name_and_count_of_games_with_last_trainer(soup=soup)
            self.scraper.scrap_match_table_data(soup=soup)
            statistics_name = self.scraper.scrap_statistic_name(soup=soup)

            self.validation_goal_data(statistics_name=statistics_name)
            for button in self.driver.buttons.get_smart_stats_buttons()[1:]:
                button.click()
                self.refresh_page()
                # self.wait_for_elements()
                time.sleep(1)
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scraper.scrap_match_table_data(soup=soup)

            self.scrap_accordion_data()

            return True

        except IndexError:
            print(
                'GameCollectorError catch INDEX ERROR in address: '
                'line/control_units/managers/games_collector/GameCollector.get_match_data()')
            return None

    def validation_goal_data(self, statistics_name, threshold=26):
        if not (len(self.all_match_data[statistics_name]['home_collections']) > threshold and len(
                self.all_match_data[statistics_name]['away_collections']) > threshold):
            print(f"MatchManagerValidError: managers.match.MatchManager.get_match_data()")
            print(f"{self.all_match_data['home_command_name']} - {self.all_match_data['away_command_name']}")
            print(f"{len(self.all_match_data[statistics_name]['home_collections'])} > {threshold}")
            print(f"{len(self.all_match_data[statistics_name]['away_collections'])} > {threshold}")
            raise AttributeError

    def refresh_page(self) -> None:
        try:
            self.driver.buttons.get_refresh_button().click()
        except NoSuchElementException:
            pass

    def wait_for_elements(self) -> None:
        WebDriverWait(self.driver.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card"]')))
