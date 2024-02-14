import time

from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.game_scraper import RealTimeGameScraper
from utils.error import ContinueError
from utils.func import is_valid_name, get_today_date
from utils.pickle_manager import PickleHandler


class GameDataCollector:
    def __init__(self, driver: LiveChromeDriver):
        self.driver = driver
        self.line_data = {}

    def collect(self):
        buttons = self.driver.driver.find_elements(By.XPATH, f'//a[contains(@class, "filter-item-event--20qx1S")]')
        for element in buttons:
            try:
                key = element.text
            except WebDriverException:
                continue
            if is_valid_name(name=key) and self.click_element(element):
                self.wait_for_info_elements()
                try:
                    self.click_filter_games(key=key)
                except ContinueError:
                    continue
        PickleHandler().write_data(data=self.line_data, path_to_file=f'data/{get_today_date()}_AllLineData.pkl')


    def click_filter_games(self, key, smart=True):
        xpath = f'//a[contains(@class, "filter-item-event--20qx1S") and starts-with(normalize-space(), "{key}")]'
        if not self.click_element(xpath):
            raise ContinueError
        if smart:
            self.wait_for_elements()
            # time.sleep(0.5)
            self.scraper = RealTimeGameScraper()
            if self.driver.buttons.is_match_button_clicked():
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scrape_team_names(soup=soup)
                self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
            else:
                try:
                    self.driver.buttons.get_match_button().click()
                    self.wait_for_elements()
                    time.sleep(0.5)
                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                    self.scrape_team_names(soup=soup)
                    self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
                except (NoSuchElementException, StaleElementReferenceException):
                    raise ContinueError
            try:
                self.stats_filter(key=key)
            except ContinueError:
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                try:
                    self.collect_game_info(soup)
                except AttributeError:
                    raise ContinueError
                self.add_default_values(key=key)

    def click_element(self, element_or_xpath):
        try:
            element = self.driver.driver.find_element(
                By.XPATH, element_or_xpath) if isinstance(element_or_xpath, str) else element_or_xpath
            try:
                element.click()
            except StaleElementReferenceException:
                return
            except ElementClickInterceptedException:
                # Scroll to the element before clicking
                self.driver.driver.execute_script("arguments[0].scrollIntoView();", element)
                # Click on the element using an offset position
                actions = ActionChains(self.driver.driver)
                actions.move_to_element(element).move_by_offset(10, 10).click().perform()
                element.click()
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            return
        return True

    def stats_filter(self, key, smart=True):
        try:
            stats_button = self.driver.buttons.get_stats_button()
        except NoSuchElementException:
            raise ContinueError
        if stats_button:
            try:
                stats_button.click()
            except StaleElementReferenceException:
                raise ContinueError
            self.wait_for_info_elements()
            time.sleep(0.5)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            if not smart:
                self.scrape_team_names(soup=soup)
            for stat_key in RealTimeGameScraper.keys:
                self.scraper.collect_stats(soup=soup, match_stat=stat_key, **RealTimeGameScraper.keys[stat_key])
                self.scraper.scrape_match_stats(soup=soup)
            try:
                self.collect_game_info(soup=soup)
                self.add_default_values(key=key)
            except AttributeError:
                raise ContinueError

    def collect_game_info(self, soup):
        try:
            self.scraper.scrape_league(soup=soup)
            self.scraper.scrape_match_score(soup=soup)
            self.scraper.scrape_match_time(soup=soup)
            self.scraper.scrape_red_cards(soup=soup)
        except AttributeError:
            time.sleep(1)
            self.scraper.scrape_league(soup=soup)
            self.scraper.scrape_match_score(soup=soup)
            self.scraper.scrape_match_time(soup=soup)
            self.scraper.scrape_red_cards(soup=soup)

    def wait_for_info_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "ev-scoreboard")]')))
        except TimeoutException:
            pass

    def wait_for_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "event-view-control--64c7OE")]')))
        except TimeoutException:
            pass

    def scrape_team_names(self, soup):
        try:
            self.scraper.scrape_line_team_names(soup=soup)
        except AttributeError:
            try:
                time.sleep(1)
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scraper.scrape_line_team_names(soup=soup)
            except AttributeError as e:
                print('scrape_team_names error', e)
                raise ContinueError

    def add_default_values(self, key):
        self.line_data[key] = {}
        self.line_data[key]['fouls_red_rate'] = None
        self.line_data[key]['yellow_red_rate'] = None
        self.line_data[key]['yellow_rate'] = None
        self.line_data[key].update(self.scraper.get_game_info())
