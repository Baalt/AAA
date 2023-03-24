from selenium.webdriver.common.by import By


class SmartStatButtons:
    def __init__(self):
        self.browser = None

    def get_smart_stats_buttons(self, selector="//div[@class='btn-group py-1 mr-2 stat-picker']//button"):
        # Find all the button elements using XPath
        buttons = self.browser.find_elements(By.XPATH, selector)
        # Filter out buttons with specific texts
        filtered_buttons = [button for button in buttons if
                            button.text.strip() not in ["Атаки", "Оп. атаки", "КК", "Другое"]]
        # Return the sorted buttons list
        return filtered_buttons

    def get_other_button(self, button_text):
        selector = f"//div[@class='btn-group py-1 mr-2 stat-picker']//button[normalize-space()='{button_text}']"
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def get_drop_down_button(self, button_text):
        selector = f"//a[@class='dropdown-item' and normalize-space()='{button_text}']"
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def get_previous_season_button(self, idx):
        button = self.browser.find_elements(By.XPATH, "//div[@id='teamsSeasons']//button")
        return button[idx]

    def get_refresh_button(self):
        selector = "//button[contains(text(),'Обновить (Enter)')]"
        button = self.browser.find_element(By.XPATH, selector)
        return button