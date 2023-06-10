from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class RefereeButtons:
    def __init__(self):
        self.browser = None

    def check_and_press_referee_button(self, selector="//a[starts-with(normalize-space(), 'Рефери')]"):
        try:
            # Find the button element by searching for the anchor tag with specific text
            button = self.browser.find_element(By.XPATH, selector)

            # Click the button if it exists
            button.click()
            return True
        except NoSuchElementException:
            return False

    def filter_table_by_matches(self, number='100'):

        # Find the input element
        input_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "manual-howmuch-input"))
        )

        # Clear the input field and enter the number
        input_element.clear()
        input_element.send_keys(number)

        # Find the button element
        button_element = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "manual-howmuch-button"))
        )

        # Click the button
        button_element.click()

    def click_current_league_button(self, league: str):
        button = self.browser.find_element(
            By.XPATH,
            f'(//div[@id="refCompetitions"])/button[normalize-space(text())=\'{league}\']')
        button.click()

    def click_all_season_button(self):
        button = self.browser.find_element(
            By.XPATH,
            '(//div[@id="teamsSeasons"])/button[last()]')
        button.click()
