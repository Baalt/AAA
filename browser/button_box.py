from browser.live_buttons.game_buttons import LiveGameButtons
from browser.live_buttons.menu_buttons import LanguageButtons, FootballMenuButtons
from browser.smart_buttons.smart_buttons import SmartStatButtons
from browser.smart_buttons.game_buttons import SmartGameButtons


class Buttons(LanguageButtons,
              FootballMenuButtons,
              LiveGameButtons,
              SmartStatButtons,
              SmartGameButtons):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
