from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GameButtons:
    def __init__(self):
        self.browser = None

    def get_match_button(self, selector="//div[contains(@class, 'tab--4RNtVz') and contains(text(), 'Match')]"):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector)))
        return button

    def is_match_button_clicked(self, selector="//div[contains(@class, 'tab--4RNtVz _state_selected--408s1N') and contains(text(), 'Match')]"):
        try:
            button = self.browser.find_element(By.XPATH, selector)
            if button:
                return True
        except NoSuchElementException:
            return False

    def get_stats_button(self, selector="//div[contains(@class, 'tab--4RNtVz') and contains(text(), 'Team stats')]"):
        button = self.browser.find_element(By.XPATH, selector)
        return button
