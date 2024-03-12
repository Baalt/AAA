import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException, WebDriverException
from bs4 import BeautifulSoup

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.game_scraper import RealTimeGameScraper
from live.analytics.match_analyzer import RedLiveCompare, SmartLiveCompare
from utils.error import ContinueError


class WebCrawler:
    def __init__(self, driver: LiveChromeDriver, smart_data: dict, league_data: dict,
                 line_data: dict, tel, excluded_games: dict):
        self.driver = driver
        self.smart_data = smart_data
        self.league_data = league_data
        self.line_data = line_data
        self.tel = tel
        self.first_time_scanned = True
        self.excluded_games = excluded_games

    async def run_crawler(self):
        start_time = time.time()
        await self.click_all_games()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 30:
            time.sleep(30 - elapsed_time)
        elif elapsed_time >= 30:
            print(f"click_filter_games took {elapsed_time} seconds to complete")

    async def click_all_games(self):
        if self.first_time_scanned:
            buttons_xpath = f'//a[contains(@class, "filter-item-event--20qx1S")]'
            buttons = self.driver.driver.find_elements(By.XPATH, buttons_xpath)
            for element in buttons:
                try:
                    key = element.text
                except WebDriverException:
                    continue
                if self.is_valid_name(name=key) and key not in self.smart_data:
                    if self.click_element(element):
                        try:
                            self.wait_for_info_elements()
                            self.scraper = RealTimeGameScraper()
                            await self.stats_filter(key=key, first_time=True)
                        except (ContinueError, KeyError):
                            continue
            print(f'number of scanned free games {len(self.excluded_games)}')
            self.first_time_scanned = None
        else:
            await self.click_filter_games(keys=self.smart_data, smart=True)
            await self.click_filter_games(keys=self.excluded_games)

    async def click_filter_games(self, keys, smart=None):
        for key in keys:
            xpath = f'//a[contains(@class, "filter-item-event--20qx1S") and starts-with(normalize-space(), "{key}")]'
            if not self.click_element(xpath):
                continue
            if smart:
                self.wait_for_elements()
                time.sleep(0.5)
                self.scraper = RealTimeGameScraper()
                if self.driver.buttons.is_match_button_clicked():
                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                    self.scrape_team_names(soup=soup)
                    self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
                else:
                    try:
                        self.driver.buttons.get_match_button().click()
                        self.wait_for_elements()
                        # time.sleep(0.5)
                        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                        try:
                            self.scraper.scrape_team_names(soup=soup)
                        except AttributeError:
                            try:
                                time.sleep(1)
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                self.scraper.scrape_team_names(soup=soup)
                            except AttributeError as e:
                                print('scrape_team_names error', e)
                                continue
                        self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                try:
                    self.driver.buttons.get_stats_button()
                except NoSuchElementException:
                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                    try:
                        self.collect_game_info(soup)
                    except AttributeError:
                        continue
                    # pprint(self.scraper.get_game_info())
                    await SmartLiveCompare(smart_data=self.smart_data[key],
                                           live_data=self.scraper.get_game_info(),
                                           league_data=self.league_data,
                                           telegram=self.tel).compare()
                try:
                    await self.stats_filter(key=key, smart=True)
                except ContinueError:
                    continue
            else:
                self.wait_for_elements()
                self.scraper = RealTimeGameScraper()
                try:
                    await self.stats_filter(key=key)
                except ContinueError:
                    continue

    async def stats_filter(self, key, smart=None, first_time=None):
        try:
            stats_button = self.driver.buttons.get_stats_button()
        except NoSuchElementException:
            raise ContinueError
        if stats_button:
            try:
                stats_button.click()
            except StaleElementReferenceException:
                raise ContinueError
            time.sleep(0.5)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            if not smart:
                self.scrape_team_names(soup=soup)
            for stat_key in RealTimeGameScraper.keys:
                self.scraper.collect_stats(soup=soup, match_stat=stat_key, **RealTimeGameScraper.keys[stat_key])
                self.scraper.scrape_match_stats(soup=soup)
            try:
                self.wait_for_info_elements()
                self.collect_game_info(soup=soup)
            except AttributeError:
                raise ContinueError

            live_data = self.scraper.get_game_info()
            if 'yellow cards' in live_data or 'fouls' in live_data:
                if first_time:
                    try:
                       self.excluded_games[key]
                    except KeyError:
                        self.excluded_games[key] = {
                            'red_foul': True,
                            'red_yellow': True,
                            'hand_yellow': True
                        }
                await RedLiveCompare(live_data=live_data,
                                     line_data=self.line_data,
                                     telegram=self.tel,
                                     excluded_games=self.excluded_games,
                                     game_key=key).compare()

            if smart:
                await SmartLiveCompare(smart_data=self.smart_data[key],
                                       live_data=live_data,
                                       league_data=self.league_data,
                                       telegram=self.tel).compare()

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

    def scrape_team_names(self, soup):
        try:
            self.scraper.scrape_team_names(soup=soup)
        except AttributeError:
            try:
                time.sleep(1)
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scraper.scrape_team_names(soup=soup)
            except AttributeError as e:
                print('scrape_team_names error', e)
                raise ContinueError

    def wait_for_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "tables--SkIhq")]')))
        except TimeoutException:
            pass

    def wait_for_info_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "event-view__header__scoreboard-container")]')))
        except TimeoutException:
            pass

    def get_live_data(self):
        self.scraper.get_game_info()

    def is_valid_name(self, name):
        return '(' not in name and '-pro' not in name and not re.search('U\d\d', name)
