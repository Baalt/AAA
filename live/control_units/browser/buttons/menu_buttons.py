from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LanguageButtons:
    def __init__(self):
        self.browser = None

    def get_select_language_button(self, selector='a.header__lang-item'):
        button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return button

    def get_select_english_button(self, selector='//span[text()="English"]'):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector)))
        return button


class FootballMenuButtons:
    def __init__(self):
        self.browser = None

    def get_select_football_category_button(self,
                                            selector='//div[contains(@class, "vertical-panel__grow")]'
                                                     '//div[contains(@class, "filter-component-row-container")][1]'
                                                     '//span[contains(@class, "filter-component-expander__arrow--5izki")]'):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector)))
        return button

    def get_select_show_all_button(self, selector='//span[text()="Show all"]'):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector)))
        return button

    def get_select_all_leagues_buttons(
            self,
            selector='//div[contains(@class, "vertical-panel__grow")]'
                     '//div[contains(@class, "filter-component-row-container")][1]'
                     '//span[contains(@class, "filter-component-expander--2CxuU")]'):
        buttons = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, selector)))
        return buttons

class Buttons(LanguageButtons, FootballMenuButtons):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
