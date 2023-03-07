from live.control_units.browser.buttons.game_buttons import GameButtons
from live.control_units.browser.buttons.menu_buttons import LanguageButtons, FootballMenuButtons


class Buttons(LanguageButtons, FootballMenuButtons, GameButtons):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
