from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from browser.live_buttons.button_box import Buttons


class HeadlessChromeDriver:
    def __init__(self, driver_path: str = '/usr/local/bin/chromedriver', headless: bool = True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.buttons = Buttons(browser=self.driver)
        self.html = None

    def open_page(self, url):
        self.driver.execute_script("window.location.href = '{}';".format(url))

    def get_page_html(self):
        return self.driver.page_source

    def maximize_window(self):
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()
