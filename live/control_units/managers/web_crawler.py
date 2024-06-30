import time
# from pprint import pprint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup

from browser.browser import LiveChromeDriver
from live.control_units.managers.tasks.main_operations import FootballMenuHandler
from live.control_units.scrapers.game_scraper import RealTimeGameScraper
from live.analytics.match_analyzer import RedLiveCompare, SmartLiveCompare, ScoreCompare
from utils.error import ContinueError


class WebCrawler(FootballMenuHandler):
    def __init__(self, driver: LiveChromeDriver, smart_data: dict, league_data: dict, line_data: dict, tel,
                 excluded_games: dict):
        super().__init__(driver)
        self.driver = driver
        self.smart_data = smart_data
        self.league_data = league_data
        self.line_data = line_data
        self.tel = tel
        self.first_time_scanned = True
        self.excluded_games = excluded_games
        self.scannable_games = []
        self.games_xpath = '//a[contains(@class, "filter-item-event-container")]'

    async def run_crawler(self):
        start_time = time.time()
        await self.click_all_games()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)
        elif elapsed_time >= 60:
            print(f"click_filter_games took {elapsed_time} seconds to complete")

    async def click_all_games(self):
        if self.first_time_scanned:
            first_time_lst = []
            self.scroll_up()
            time.sleep(2)
            while True:
                all_buttons = self.driver.driver.find_elements(
                    By.XPATH,
                    f'//a[contains(@class, "filter-item-event-container")]'
                )
                buttons = []
                for button in all_buttons:
                    try:
                        if button.text not in first_time_lst:
                            buttons.append(button)
                    except StaleElementReferenceException:
                        continue

                if not buttons:
                    self.scroll_page_down()
                    time.sleep(2)
                    all_buttons = self.driver.driver.find_elements(
                        By.XPATH,
                        '//a[contains(@class, "filter-item-event-container")]'
                    )
                    buttons = []
                    for button in all_buttons:
                        try:
                            if button.text not in first_time_lst:
                                buttons.append(button)
                        except StaleElementReferenceException:
                            continue
                    if not buttons:
                        break

                for button in buttons:
                    try:
                        button.click()
                        key = button.text
                        first_time_lst.append(key)
                        self.browser.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", button)
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        continue
                    if not self.is_valid_name(key):
                        continue
                    try:
                        time.sleep(1)
                        stats_button = self.driver.buttons.get_stats_button()
                    except NoSuchElementException:
                        continue
                    if stats_button:
                        try:
                            stats_button.click()
                            time.sleep(1)
                        except (StaleElementReferenceException, ElementClickInterceptedException):
                            continue
                        try:
                            if self.driver.buttons.is_cards_button('Yellow cards') or \
                                    self.driver.buttons.is_cards_button('Fouls'):
                                try:
                                    self.excluded_games[key]
                                except KeyError:
                                    self.excluded_games[key] = {
                                        'red_yellow': True,
                                        'score_under': True,
                                        'score_mix': True
                                    }
                                self.scannable_games.append(key)
                                self.wait_for_elements()
                                self.scraper = RealTimeGameScraper()
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                self.collect_game_info(soup=soup)

                                if self.driver.buttons.is_cards_button('Yellow cards'):
                                    self.driver.buttons.get_cards_button('Yellow cards').click()
                                    time.sleep(0.5)
                                    self.wait_for_elements()
                                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                    for stat_key in RealTimeGameScraper.keys:
                                        self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                                   **RealTimeGameScraper.keys[stat_key])

                                    if self.excluded_games[key]['score_under']:
                                        await ScoreCompare(live_data=self.scraper.get_game_info(),
                                                           telegram=self.tel,
                                                           excluded_games=self.excluded_games,
                                                           game_key=key).compare()

                                if self.driver.buttons.is_cards_button('Fouls'):
                                    self.driver.buttons.get_cards_button('Fouls').click()
                                    time.sleep(0.5)
                                    self.wait_for_elements()
                                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                    for stat_key in RealTimeGameScraper.keys:
                                        self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                                   **RealTimeGameScraper.keys[stat_key])
                                    c = RedLiveCompare(live_data=self.scraper.get_game_info(),
                                                       telegram=self.tel,
                                                       excluded_games=self.excluded_games,
                                                       game_key=key)

                                    if self.excluded_games[key]['red_yellow']:
                                        await c.compare()
                                    if self.excluded_games[key]['score_mix']:
                                        await c.compare_mix()

                                if key in self.smart_data:
                                    await SmartLiveCompare(smart_data=self.smart_data[key],
                                                           live_data=self.scraper.get_game_info(),
                                                           league_data=self.league_data,
                                                           telegram=self.tel).compare()
                        except NoSuchElementException:
                            # print('click_all_games.ERROR:', e)
                            continue
            self.first_time_scanned = None
        else:
            await self.click_scannable_games()

    async def click_scannable_games(self):
        round_lst = []
        self.scroll_up()
        time.sleep(2)
        while True:
            all_buttons = self.driver.driver.find_elements(
                By.XPATH,
                f'//a[contains(@class, "filter-item-event-container")]'
            )
            buttons = []
            for button in all_buttons:
                try:
                    if button.text not in round_lst:
                        buttons.append(button)
                except StaleElementReferenceException:
                    continue

            if not buttons:
                self.scroll_page_down()
                time.sleep(2)
                all_buttons = self.driver.driver.find_elements(
                    By.XPATH,
                    '//a[contains(@class, "filter-item-event-container")]'
                )
                buttons = []
                for button in all_buttons:
                    try:
                        if button.text not in round_lst:
                            buttons.append(button)
                    except StaleElementReferenceException:
                        continue
                if not buttons:
                    # Try clicking the last button
                    try:
                        last_button = all_buttons[-1]
                        self.browser.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", last_button)
                        last_button.click()
                    except IndexError:
                        pass
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        # If the last button fails, try the penultimate button
                        try:
                            penultimate_button = all_buttons[-2]
                            self.browser.driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center'});", penultimate_button)
                            penultimate_button.click()
                        except IndexError:
                            pass
                        except (StaleElementReferenceException, ElementClickInterceptedException):
                            pass
                    break

            for button in buttons:
                try:
                    self.browser.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", button)
                    key = button.text
                    if key in self.scannable_games:
                        button.click()
                        round_lst.append(key)
                    else:
                        round_lst.append(key)
                        continue
                except (StaleElementReferenceException, ElementClickInterceptedException):
                    continue
                try:
                    time.sleep(1)
                    stats_button = self.driver.buttons.get_stats_button()
                except NoSuchElementException:
                    continue
                if stats_button:
                    try:
                        stats_button.click()
                        time.sleep(1)
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        continue
                    try:
                        if self.driver.buttons.is_cards_button('Yellow cards') or \
                                self.driver.buttons.is_cards_button('Fouls'):
                            self.wait_for_elements()
                            self.scraper = RealTimeGameScraper()
                            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                            self.collect_game_info(soup=soup)

                            if self.driver.buttons.is_cards_button('Yellow cards'):
                                self.driver.buttons.get_cards_button('Yellow cards').click()
                                time.sleep(0.5)
                                self.wait_for_elements()
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                for stat_key in RealTimeGameScraper.keys:
                                    self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                               **RealTimeGameScraper.keys[stat_key])

                                if self.excluded_games[key]['score_under']:
                                    await ScoreCompare(live_data=self.scraper.get_game_info(),
                                                       telegram=self.tel,
                                                       excluded_games=self.excluded_games,
                                                       game_key=key).compare()

                            if self.driver.buttons.is_cards_button('Fouls'):
                                self.driver.buttons.get_cards_button('Fouls').click()
                                time.sleep(0.5)
                                self.wait_for_elements()
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                for stat_key in RealTimeGameScraper.keys:
                                    self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                               **RealTimeGameScraper.keys[stat_key])

                                c = RedLiveCompare(live_data=self.scraper.get_game_info(),
                                                   telegram=self.tel,
                                                   excluded_games=self.excluded_games,
                                                   game_key=key)

                                if self.excluded_games[key]['red_yellow']:
                                    await c.compare()
                                if self.excluded_games[key]['score_mix']:
                                    await c.compare_mix()
                            if key in self.smart_data:
                                await SmartLiveCompare(smart_data=self.smart_data[key],
                                                       live_data=self.scraper.get_game_info(),
                                                       league_data=self.league_data,
                                                       telegram=self.tel).compare()
                            # pprint(self.scraper.get_game_info())
                    except NoSuchElementException:
                        # print('click_all_games.ERROR:', e)
                        continue

    def collect_game_info(self, soup):
        try:
            self.scraper.scrape_league(soup)
            self.scraper.scrape_game_info(soup)
            self.scraper.scrape_match_stats(soup)
        except AttributeError:
            time.sleep(1)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_league(soup)
                self.scraper.scrape_game_info(soup)
                self.scraper.scrape_match_stats(soup)
            except AttributeError as e:
                print('collect_game_info', e)
                raise ContinueError

    def wait_for_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "sport-footer__wrap")]')))
        except TimeoutException:
            pass

    def get_live_data(self):
        self.scraper.get_game_info()
