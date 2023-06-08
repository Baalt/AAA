import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup

from browser.browser import LiveChromeDriver
from live.control_units.scrapers.game_scraper import RealTimeGameScraper
from live.analytics.match_analyzer import SmartLiveCompare


class WebCrawler:
    def __init__(self, driver: LiveChromeDriver, smart_data: dict, league_data: dict, tel):
        self.driver = driver
        self.smart_data = smart_data
        self.league_data = league_data
        self.tel = tel

    async def run_crawler(self):
        start_time = time.time()
        await self.click_filter_games()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 30:
            time.sleep(30 - elapsed_time)
        elif elapsed_time >= 30:
            print(f"click_filter_games took {elapsed_time} seconds to complete")

    async def click_filter_games(self):
        for key in self.smart_data:
            xpath = f'//a[contains(@class, "filter-item-event--20qx1S") and starts-with(normalize-space(), "{key}")]'
            if not self.click_element_by_xpath(xpath):
                continue

            self.wait_for_elements()
            # time.sleep(0.5)
            self.scraper = RealTimeGameScraper()
            if self.driver.buttons.is_match_button_clicked():
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
                stats_button = self.driver.buttons.get_stats_button()
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
                continue

            if stats_button:
                try:
                    stats_button.click()
                except StaleElementReferenceException:
                    continue
                # time.sleep(1)
                self.wait_for_elements()
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                for stat_key in RealTimeGameScraper.keys:
                    self.scraper.collect_stats(soup=soup, match_stat=stat_key, **RealTimeGameScraper.keys[stat_key])
                    self.scraper.scrape_match_stats(soup=soup)
                try:
                    self.collect_game_info(soup)
                except AttributeError:
                    continue
                # pprint(self.scraper.get_game_info())
                await SmartLiveCompare(smart_data=self.smart_data[key],
                                       live_data=self.scraper.get_game_info(),
                                       league_data=self.league_data,
                                       telegram=self.tel).compare()

    def click_element_by_xpath(self, xpath):
        try:
            element = self.driver.driver.find_element(By.XPATH, xpath)
            try:
                element.click()
            except StaleElementReferenceException:
                return False
            except ElementClickInterceptedException :
                # Scroll to the element before clicking
                self.driver.driver.execute_script("arguments[0].scrollIntoView();", element)
                # Click on the element using an offset position
                actions = ActionChains(self.driver.driver)
                actions.move_to_element(element).move_by_offset(10, 10).click().perform()
                element.click()
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            return False
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

    def wait_for_elements(self):
        try:
            WebDriverWait(self.driver.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "event-view-control--64c7OE")]')))
        except TimeoutException:
            pass

    def get_live_data(self):
        self.scraper.get_game_info()
