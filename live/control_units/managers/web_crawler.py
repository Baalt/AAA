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

    def click_filter_games(self):
        for key in self.smart_data:
            xpath = f'//a[contains(@class, "filter-item-event--20qx1S") and starts-with(normalize-space(), "{key}")]'
            try:
                element = self.driver.driver.find_element(By.XPATH, xpath)
                print(f"{key} = {element.text}")
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
                continue

            WebDriverWait(self.driver.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
            self.scraper = RealTimeGameScraper()
            if self.driver.buttons.is_match_button_clicked():
                print('Кнопка Матч уже была нажата, я просто скрмыш')
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                self.scraper.collect_stats(soup=soup, match_stat='goals', **RealTimeGameScraper.keys['goals'])
            else:
                try:
                    if self.driver.buttons.get_match_button():
                        print('Кнопка не была нажата, но существует, я её нажимаю и скрмыш')
                        self.driver.buttons.get_match_button().click()
                        WebDriverWait(self.driver.driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//*')))
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
                print('кнопка статистики не существуют')
                continue

            if stats_button:
                print('cуществует кнопка cтатистики и я её нажимаю')
                stats_button.click()
                WebDriverWait(self.driver.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
                soup = BeautifulSoup(self.driver.get_page_html(), 'lxml')
                for stat_key in RealTimeGameScraper.keys:
                    self.scraper.collect_stats(soup=soup, match_stat=stat_key, **RealTimeGameScraper.keys[stat_key])
                self.scraper.scrape_match_stats(soup=soup)
                self.collect_game_info(soup)
                self.scraper.print_game_info()

    def collect_game_info(self, soup):
        self.scraper.scrape_league(soup=soup)
        self.scraper.scrape_team_names(soup=soup)
        self.scraper.scrape_match_score(soup=soup)
        self.scraper.scrape_match_time(soup=soup)
        self.scraper.scrape_red_cards(soup=soup)

    def get_live_data(self):
        self.scraper.get_game_info()
