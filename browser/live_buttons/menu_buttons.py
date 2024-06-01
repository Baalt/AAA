from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LanguageButtons:
    def __init__(self):
        self.browser = None

    def get_language_button(self, selector='a.header__lang-item'):
        button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return button

    def get_english_button(self, selector='//span[text()="English"]'):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector)))
        return button


class FootballMenuButtons:
    def __init__(self):
        self.browser = None

    def get_football_category_button(self):
        selector = '//div[contains(@class, "filter-component-row") and contains(@class, "filter-item-sport")]'
        football_div = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, selector)))
        football_text_span = football_div.find_element(By.XPATH, './/span[contains(@class, "filter-component-text")]')
        if 'Football' in football_text_span.text:
            button = football_div.find_element(By.XPATH, './/span[contains(@class, "filter-component-expander")]')
            return button
        else:
            return None

    def get_show_all_button(self, selector='//span[text()="Show all"]'):
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def get_all_leagues_buttons(
            self,
            selector='//span[@class="filter-component-expander--fx9FJ _dropDownMode--KDf2N filter-item-competition__expander--qq1th"]'):
        buttons = self.browser.find_elements(By.XPATH, selector)
        return buttons
