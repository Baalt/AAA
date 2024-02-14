from browser.browser import LiveChromeDriver
from live.control_units.managers.tasks.line_collector import GameDataCollector
from live.control_units.managers.tasks.main_operations import BrowserPreparer, FootballMenuHandler


if __name__ == '__main__':
    line_data = {}
    is_line_data_download = False
    driver = LiveChromeDriver()
    browser = BrowserPreparer(driver=driver)
    browser.open_page(url='https://www.fon.bet/sports/?mode=1') if not is_line_data_download else browser.open_page()
    browser.switch_language()
    controller = FootballMenuHandler(driver=browser.browser)
    controller.open_main_football_menu()
    controller.open_full_leagues_list()
    controller.open_all_football_leagues()

    collector = GameDataCollector(driver=driver)
    collector.collect()
