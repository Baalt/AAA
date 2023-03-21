import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup

from browser.browser import HeadlessChromeDriver
from live.control_units.scripers.game_scraper import RealTimeGameScraper


class WebCrawler:
    def __init__(self, driver: HeadlessChromeDriver, smart_data: dict):
        self.driver = driver
        self.smart_data = smart_data

    def run_crawler(self):
        start_time = time.time()
        self.click_filter_games()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 30:
            time.sleep(30 - elapsed_time)
        elif elapsed_time >= 30:
            print(f"click_filter_games took {elapsed_time} seconds to complete")


    def click_filter_games(self):
        for key in self.smart_data:
            xpath = f'//a[contains(@class, "filter-item-event--20qx1S") and starts-with(normalize-space(), "{key}")]'
            if not self.click_element_by_xpath(xpath):
                continue

            self.wait_for_elements()
            self.scraper = RealTimeGameScraper()
            if self.driver.buttons.is_match_button_clicked():
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
            else:
                try:
                    if self.driver.buttons.get_match_button():
                        self.driver.buttons.get_match_button().click()
                        self.wait_for_elements()
                        soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                        self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
                except NoSuchElementException:
                    continue
            try:
                stats_button = self.driver.buttons.get_stats_button()
            except NoSuchElementException:
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.collect_game_info(soup)
                self.scraper.print_game_info()
                continue

            if stats_button:
                stats_button.click()
                self.wait_for_elements()
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                for stat_key in RealTimeGameScraper.keys:
                    self.scraper.collect_stats(soup=soup, match_stat=stat_key, **RealTimeGameScraper.keys[stat_key])
                self.scraper.scrape_match_stats(soup=soup)
                self.collect_game_info(soup)
                self.scraper.print_game_info()

    def click_element_by_xpath(self, xpath):
        try:
            element = self.driver.driver.find_element(By.XPATH, xpath)
            try:
                element.click()
            except ElementClickInterceptedException:
                # Scroll to the element before clicking
                self.driver.driver.execute_script("arguments[0].scrollIntoView();", element)
                # Click on the element using an offset position
                actions = ActionChains(self.driver.driver)
                actions.move_to_element(element).move_by_offset(10, 10).click().perform()
                element.click()
        except NoSuchElementException:
            return False
        return True

    def collect_game_info(self, soup):
        self.scraper.scrape_league(soup=soup)
        self.scraper.scrape_team_names(soup=soup)
        self.scraper.scrape_match_score(soup=soup)
        self.scraper.scrape_match_time(soup=soup)
        self.scraper.scrape_red_cards(soup=soup)

    def wait_for_elements(self):
        WebDriverWait(self.driver.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

    def get_live_data(self):
        self.scraper.get_game_info()
