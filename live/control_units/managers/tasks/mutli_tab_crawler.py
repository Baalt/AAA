import time

from bs4 import BeautifulSoup
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException

from browser.browser import HeadlessChromeDriver
from live.control_units.scripers.game_scraper import RealTimeGameScraper


class MultiTabCrawler:
    def __init__(self, driver: HeadlessChromeDriver):
        self.driver = driver
        self.match_pedia = {}

    def show_match_pedia(self):
        from pprint import pprint
        pprint(self.match_pedia)

    def get_match_pedia(self):
        return self.match_pedia

    def collect_data_from_tabs(self):
        self.match_pedia = {}
        for handle in self.driver.driver.window_handles:
            self.driver.driver.switch_to.window(handle)
            try:
                self.click_match_button()
                self.scraper = RealTimeGameScraper()
                page_html = self.driver.get_page_html()
                soup = BeautifulSoup(page_html, 'lxml')
                self.scraper.collect_stats(soup=soup, match_stat='goals',
                                           total_text=RealTimeGameScraper.keys['goals']['total_text'],
                                           team_total_text=RealTimeGameScraper.keys['goals']['team_total_text'],
                                           handicap_text=RealTimeGameScraper.keys['goals']['handicap_text'])
            except TimeoutException as timeout_err:
                print(f"Timeout error: {timeout_err}")
                self.driver.quit()
                continue
            except NoSuchElementException as no_elem_err:
                print(f"No such element error: {no_elem_err}")
                self.driver.quit()
                continue
            except StaleElementReferenceException as stale_err:
                print(f"Stale element reference error: {stale_err}")
                self.driver.quit()
                continue

            try:
                self.click_stats_button()
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                for stat_key in RealTimeGameScraper.keys:
                    self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                               total_text=RealTimeGameScraper.keys[stat_key]['total_text'],
                                               team_total_text=RealTimeGameScraper.keys[stat_key]['team_total_text'],
                                               handicap_text=RealTimeGameScraper.keys[stat_key]['handicap_text'])
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
                pass

            try:
                self.collect_match_info(soup=soup)
                match_data: dict = self.scraper.get_game_info()
                match_key = self.get_common_name(first_team=match_data['team1_name'],
                                                 second_team=match_data['team2_name'])
                self.match_pedia.setdefault(match_key, {}).update(match_data)
            except ValueError:
                pass

    def collect_match_info(self, soup):
        self.scraper.scrape_league(soup=soup)
        self.scraper.scrape_team_names(soup=soup)
        self.scraper.scrape_match_score(soup=soup)
        self.scraper.scrape_match_stats(soup=soup)
        self.scraper.scrape_match_time(soup=soup)
        self.scraper.scrape_red_cards(soup=soup)

    def get_common_name(self, first_team, second_team, separator=' - '):
        return f"{first_team}{separator}{second_team}"

    def click_match_button(self):
        self.driver.buttons.get_match_button().click()
        time.sleep(1)

    def click_stats_button(self):
        self.driver.buttons.get_stats_button().click()
        time.sleep(1)