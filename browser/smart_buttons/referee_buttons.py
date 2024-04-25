import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

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
        input_element = WebDriverWait(self.browser, 20).until(
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

    def click_all_league_button(self):
        button = self.browser.find_element(
            By.XPATH,
            '//div[@id="refCompetitions"]/button[contains(text(), "Все")]')
        button.click()

    def click_current_league_button(self, league: str):
        button = self.browser.find_element(
            By.XPATH,
            f'(//div[@id="refCompetitions"])/button[normalize-space(text())=\'{league}\']')
        button.click()

    # def click_dropdown_button(self):
    #     try:
    #         # Find the div with the class 'dropdown'
    #         dropdown = self.browser.find_element(By.CLASS_NAME, "dropdown")
    #         # Find the button inside the div
    #         button = dropdown.find_element(By.TAG_NAME, "button")
    #         button.click()
    #     except NoSuchElementException:
    #         print("Button inside 'dropdown' div not found or could not be clicked.")
    #
    # def click_checkbox_with_text(self, text):
    #     try:
    #         WebDriverWait(self.browser, 10).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu"))
    #         )
    #
    #         # Get all checkboxes
    #         checkboxes = self.browser.find_elements(By.CLASS_NAME, "form-check-input")
    #
    #         # Iterate over the checkboxes
    #         for checkbox in checkboxes:
    #             # Get the label of the checkbox
    #             label = checkbox.find_element(By.XPATH, "./following-sibling::label")
    #             print(label)
    #
    #             # If the label text contains the desired text, click the checkbox
    #             if text in label.text:
    #                 checkbox.click()
    #                 break
    #     except NoSuchElementException:
    #         print(f"Checkbox with text '{text}' not found or could not be clicked.")

    def click_all_season_button(self):
        button = self.browser.find_element(
            By.XPATH,
            '//div[@id="teamsSeasons"]//button[contains(text(), "Все")]')

        # Scroll to the button if necessary
        actions = ActionChains(self.browser)
        actions.move_to_element(button)
        actions.perform()

        # Wait for the tooltip to disappear
        wait = WebDriverWait(self.browser, 10)
        tooltip = self.browser.find_element(By.CLASS_NAME, 'tooltip-inner')
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tooltip-inner')))

        # Use JavaScript to click the button
        self.browser.execute_script("arguments[0].click();", button)

        # Optional: Add a small delay to allow the click to take effect
        time.sleep(1)
