from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By


class LiveGameButtons:
    def __init__(self):
        self.browser = None

    def get_match_button(
            self,
            selector="//span[contains(@class, 'clear-outline--Cqh52') and contains(text(), 'Match')]"):
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def is_match_button_clicked(
            self,
            selector="//span[contains(@class, 'clear-outline--Cqh52') and contains(@class, 'selected')  and contains(text(), 'Match')]"):
        try:
            button = self.browser.find_element(By.XPATH, selector)
            if button:
                return True
        except NoSuchElementException:
            return

    def get_stats_button(
            self,
            selector="//span[contains(@class, 'clear-outline') and contains(text(), 'Team stats')]"):
        button = self.browser.find_element(By.XPATH, selector)
        return button

    def get_group_anchor_div(self):
        return self.browser.find_element(By.XPATH, "//div[contains(@class, 'group-anchor')]")

    def is_statistic_button(self, statistic):
        try:
            group_anchor_div = self.get_group_anchor_div()
            yellow_cards_span = group_anchor_div.find_element(
                By.XPATH,
                f"//span[contains(@class, 'button') and contains(text(), '{statistic}')]")
            if yellow_cards_span:
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return

    def get_statistic_button(self, statistic):
        group_anchor_div = self.get_group_anchor_div()
        yellow_cards_span = group_anchor_div.find_element(
            By.XPATH,
            f"//span[contains(@class, 'button') and contains(text(), '{statistic}')]")
        return yellow_cards_span

    def get_info_button(self):
        panel = self.browser.find_element(By.XPATH, "//div[contains(@class, 'horizontal-overflow-panel')]/div[contains(@class, 'tab-wrapper')]")
        # tab_wrappers = panel.find_elements(By.XPATH, ".//div[contains(@class, 'tab-wrapper')]")
        if panel:
            return panel
        else:
            return None

    def get_tournament_button(self):
        sport_stats_div = self.browser.find_element(By.XPATH, "//div[contains(@class, 'sport-stats-component')]")
        tournament_button = sport_stats_div.find_element(
            By.XPATH,
            ".//span[contains(@class, 'button') and contains(text(), 'Tournament')]"
        )
        return tournament_button