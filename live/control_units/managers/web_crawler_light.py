import time
import math

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from bs4 import BeautifulSoup

from live.control_units.scrapers.game_scraper_light import GameScraperLight
from live.analytics.match_analyzer import MatchAnalyzer
from utils.error import ContinueError, QuantityError

from live.control_units.managers.web_crawler import WebCrawler


class WebCrawlerLight(WebCrawler):
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
                            self.excluded_games[key]
                        except KeyError:
                            dct = {'yellow cards': '?',
                                   'fouls': '?',
                                   'fouls_line': True,
                                   'throws': True}
                            self.excluded_games[key] = dct

                        market = {
                            'yellow_market': None,
                            'foul_market': None,
                            'throw_market': None}

                        self.scraper = GameScraperLight()
                        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                        self.collect_game_info(soup)
                        try:
                            if self.driver.buttons.is_statistic_button('Yellow cards') and self.excluded_games[key][
                                'yellow cards']:
                                self.driver.buttons.get_statistic_button('Yellow cards').click()
                                time.sleep(1)
                                self.wait_for_elements()
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                for stat_key in GameScraperLight.keys:
                                    self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                               **GameScraperLight.keys[stat_key])
                                market['yellow_market'] = True

                            if self.driver.buttons.is_statistic_button('Foul') and self.excluded_games[key]['fouls']:
                                self.driver.buttons.get_statistic_button('Fouls').click()
                                time.sleep(1)
                                self.wait_for_elements()
                                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                for stat_key in GameScraperLight.keys:
                                    self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                               **GameScraperLight.keys[stat_key])
                                market['foul_market'] = True

                            if self.driver.buttons.is_statistic_button('Throw-ins') and self.excluded_games[key][
                                'throws']:
                                market['throw_market'] = True

                            if self.check_markets(market):
                                info_button = self.driver.buttons.get_info_button()
                                if info_button:
                                    info_button.click()
                                    time.sleep(1)
                                    tournament_button = self.driver.buttons.get_tournament_button()
                                    if tournament_button:
                                        tournament_button.click()
                                        time.sleep(1)
                                        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                        if self.scraper.extract_tournament_info(soup):
                                            if self.check_team_ranks(self.scraper.get_game_info()):
                                                try:
                                                    analyzer = MatchAnalyzer(
                                                        info_dict=self.scraper.get_game_info(),
                                                        market=market,
                                                        excluded_games=self.excluded_games,
                                                        game_key=key,
                                                        tel=self.tel)
                                                except QuantityError:
                                                    continue
                                                await analyzer.search()
                                                if self.check_scannable_game(market, key):
                                                    self.scannable_games.append(key)

                                            if market['throw_market'] and self.excluded_games[key]['throws']:
                                                try:
                                                    await MatchAnalyzer(
                                                        info_dict=self.scraper.get_game_info(),
                                                        market=market,
                                                        excluded_games=self.excluded_games,
                                                        game_key=key,
                                                        tel=self.tel).check_wide_throws()
                                                except QuantityError:
                                                    continue
                                                if self.excluded_games[key]['throws'] and key not in self.scannable_games:
                                                    self.scannable_games.append(key)
                                                    self.only_wide_throw_games.append(key)

                        except (NoSuchElementException, StaleElementReferenceException):
                            continue
                        if key not in self.scannable_games:
                            del self.excluded_games[key]

            self.first_time_scanned = None
            print(f'{len(self.scannable_games)} scanning games')
            print(self.scannable_games) if self.scannable_games else ...
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
                    market = {
                        'yellow_market': None,
                        'foul_market': None,
                        'throw_market': None}

                    self.scraper = GameScraperLight()
                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                    self.collect_game_info(soup)
                    try:
                        if self.driver.buttons.is_statistic_button('Yellow cards') and self.excluded_games[key][
                            'yellow cards']:
                            self.driver.buttons.get_statistic_button('Yellow cards').click()
                            time.sleep(1)
                            self.wait_for_elements()
                            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                            for stat_key in GameScraperLight.keys:
                                self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                           **GameScraperLight.keys[stat_key])
                            market['yellow_market'] = True

                        if self.driver.buttons.is_statistic_button('Foul') and self.excluded_games[key]['fouls']:
                            self.driver.buttons.get_statistic_button('Fouls').click()
                            time.sleep(1)
                            self.wait_for_elements()
                            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                            for stat_key in GameScraperLight.keys:
                                self.scraper.collect_stats(soup=soup, match_stat=stat_key,
                                                           **GameScraperLight.keys[stat_key])
                            market['foul_market'] = True

                        if self.driver.buttons.is_statistic_button('Throw-ins') and self.excluded_games[key]['throws']:
                            market['throw_market'] = True

                        if self.check_markets(market):
                            if key not in self.only_wide_throw_games:
                                try:
                                    await MatchAnalyzer(
                                        info_dict=self.scraper.get_game_info(),
                                        market=market,
                                        excluded_games=self.excluded_games,
                                        game_key=key,
                                        tel=self.tel).search()
                                except QuantityError:
                                    continue

                            if market['throw_market'] and self.excluded_games[key]['throws']:
                                try:
                                    await MatchAnalyzer(
                                        info_dict=self.scraper.get_game_info(),
                                        market=market,
                                        excluded_games=self.excluded_games,
                                        game_key=key,
                                        tel=self.tel).check_wide_throws()
                                except QuantityError:
                                    continue

                    except NoSuchElementException:
                        # print('click_all_games.ERROR:', e)
                        continue

    def check_markets(self, dct):
        if dct['yellow_market'] or dct['foul_market'] or dct['throw_market']:
            return True

    def check_scannable_game(self, dct, key):
        if (self.excluded_games[key]['yellow cards'] and dct[
            'yellow_market']) or (self.excluded_games[key]['fouls'] and dct[
            'foul_market']) or (self.excluded_games[key]['throws'] and dct['throw_market']):
            return True

    def check_team_ranks(self, data, percent=0.25):
        total_teams = data.get("total_teams")
        tournament_info = data.get("tournament_info", [])

        if not total_teams or not tournament_info:
            return

        upper_rank_threshold = math.ceil(total_teams * percent)
        lower_rank_threshold = total_teams - upper_rank_threshold + 1

        top_ranks = {1, 2}  # Две верхние команды
        bottom_ranks = {total_teams, total_teams - 1}  # Две нижние команды

        has_top_team = any(int(team["rank"]) in top_ranks for team in tournament_info)
        has_bottom_team = any(int(team["rank"]) in bottom_ranks for team in tournament_info)

        has_upper_rank_team = any(int(team["rank"]) <= upper_rank_threshold for team in tournament_info)
        has_lower_rank_team = any(int(team["rank"]) >= lower_rank_threshold for team in tournament_info)

        if (has_top_team and has_lower_rank_team) or (has_bottom_team and has_upper_rank_team):
            return True

    def collect_game_info(self, soup):
        try:
            self.scraper.scrape_league(soup)
            self.scraper.scrape_game_info(soup)
        except AttributeError:
            time.sleep(1)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_league(soup)
                self.scraper.scrape_game_info(soup)
            except AttributeError as e:
                print('collect_game_info', e)
                raise ContinueError
