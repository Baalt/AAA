import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from bs4 import BeautifulSoup


from live.control_units.scrapers.game_scraper_light import GameScraperLight
from live.analytics.match_analyzer import MatchAnalyzer
from utils.error import ContinueError

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
                    # if not self.is_valid_name(key):
                    #     continue
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
                            if self.driver.buttons.is_statistic_button('Throw-ins'):
                                time.sleep(1)
                                info_button = self.driver.buttons.get_info_button()
                                if info_button:
                                    info_button.click()
                                    time.sleep(1)
                                    tournament_button = self.driver.buttons.get_tournament_button()
                                    if tournament_button:
                                        tournament_button.click()
                                        time.sleep(1)

                                        self.scraper = GameScraperLight()
                                        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                        self.collect_game_info(soup=soup)
                                        self.scraper.show_game_info()
                                        if self.check_match_time(self.scraper.get_game_info()):
                                            try:
                                                self.excluded_games[key]
                                            except KeyError:
                                                self.excluded_games[key] = {'check': True}
                                            if self.excluded_games['check']:
                                                await MatchAnalyzer(
                                                    info_dict=self.scraper.game_info(),
                                                    excluded_games=self.excluded_games,
                                                    game_key=key,
                                                    tel=self.tel
                                                ).check_conditions()
                                                if self.excluded_games['check']:
                                                    self.scannable_games.append(key)

                        except NoSuchElementException:
                            # print('click_all_games.ERROR:', e)
                            continue
            self.first_time_scanned = None
            print(f'{len(self.scannable_games)} scanning_games')
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
                        if self.driver.buttons.is_statistic_button('Throw-ins'):
                            time.sleep(1)
                            info_button = self.driver.buttons.get_info_button()
                            if info_button:
                                info_button.click()
                                time.sleep(1)
                                tournament_button = self.driver.buttons.get_tournament_button()
                                if tournament_button:
                                    tournament_button.click()
                                    time.sleep(1)

                                    self.scraper = GameScraperLight()
                                    soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                                    self.collect_game_info(soup=soup)
                                    self.scraper.show_game_info()
                                    if self.excluded_games[key]['check'] and self.check_match_time(
                                        self.scraper.get_game_info()):
                                        await MatchAnalyzer(
                                            info_dict=self.scraper.game_info(),
                                            excluded_games=self.excluded_games,
                                            game_key=key,
                                            tel=self.tel
                                        ).check_conditions()
                    except NoSuchElementException:
                        # print('click_all_games.ERROR:', e)
                        continue

    def check_match_time(self, data: dict, max_minute=60):
        match_time = data.get('match_time')
        if match_time and ':' in match_time:
            minutes = int(match_time.split(':')[0])
            if minutes < max_minute:
                return True
        return None

    def collect_game_info(self, soup):
        try:
            self.scraper.scrape_league(soup)
            self.scraper.scrape_game_info(soup)
            self.scraper.extract_tournament_info(soup)
        except AttributeError:
            time.sleep(1)
            soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
            try:
                self.scraper.scrape_league(soup)
                self.scraper.scrape_game_info(soup)
                self.scraper.extract_tournament_info(soup)
            except AttributeError as e:
                print('collect_game_info', e)
                raise ContinueError
