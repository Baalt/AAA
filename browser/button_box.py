from browser.live_buttons.game_buttons import LiveGameButtons
from browser.live_buttons.menu_buttons import LanguageButtons, FootballMenuButtons
from browser.smart_buttons.smart_buttons import SmartStatButtons
from browser.smart_buttons.game_buttons import SmartGameButtons
from browser.smart_buttons.referee_buttons import RefereeButtons

class Buttons(LanguageButtons,
              FootballMenuButtons,
              LiveGameButtons,
              SmartStatButtons,
              SmartGameButtons,
              RefereeButtons):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
