import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SmartStatButtons:
    def __init__(self):
        self.browser = None

    def get_smart_stats_buttons(self, selector="//div[@class='btn-group py-1 mr-2 stat-picker']//button"):
        # Define the desired order of buttons
        button_order = ['Голы', 'Угловые', 'ЖК', 'Офсайды', 'Фолы', 'Уд. в створ', 'Ауты']

        # Find all the button elements using XPath
        buttons = self.browser.find_elements(By.XPATH, selector)

        # Filter out buttons with specific texts
        filtered_buttons = [button for button in buttons if button.text.strip() in button_order]

        # Sort the buttons based on the desired order
        sorted_buttons = sorted(filtered_buttons, key=lambda btn: button_order.index(btn.text.strip()))

        return sorted_buttons

    def get_fouls_button(self, selector="//div[@class='btn-group py-1 mr-2 stat-picker']//button"):
        # Get all buttons using the existing method
        buttons = self.get_smart_stats_buttons(selector)

        # Iterate through buttons and find the one with the text 'Фолы'
        for button in buttons:
            if button.text.strip() == 'Фолы':
                return button


    def get_other_button(self, selector="//button[contains(@class, 'dropdown-toggle')]"):
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def get_drop_down_button(self, button_text, timeout=10):
        selector = f"//a[@class='dropdown-item' and contains(text(), '{button_text}')]"
        wait = WebDriverWait(self.browser, timeout)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
        return button

    def get_all_season_button(self):
        button = self.browser.find_element(By.XPATH, "//div[@id='teamsSeasons']//button[contains(text(), 'Все')]")
        return button

    def get_previous_season_buttons(self):
        buttons = self.browser.find_elements(By.XPATH, "//div[@id='teamsSeasons']//button")
        matching_buttons = []
        for button in buttons:
            if re.search('\d{4}', button.text):
                matching_buttons.append(button)
        return matching_buttons

    def get_refresh_button(self):
        selector = "//button[contains(text(),'Обновить (Enter)')]"
        button = self.browser.find_element(By.XPATH, selector)
        return button
