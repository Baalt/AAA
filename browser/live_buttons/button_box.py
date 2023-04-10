from browser.live_buttons.game_buttons import GameButtons
from browser.live_buttons.menu_buttons import LanguageButtons, FootballMenuButtons
from browser.smart_buttons.smart_buttons import SmartStatButtons


class Buttons(LanguageButtons,
              FootballMenuButtons,
              GameButtons, SmartStatButtons):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
