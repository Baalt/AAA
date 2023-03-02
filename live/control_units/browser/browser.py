from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from async_live.control_units.browser.buttons.menu_buttons import Buttons


class HeadlessChromeDriver:
    def __init__(self, driver_path: str = '/usr/local/bin/chromedriver', headless: bool = True):
        options = Options()
        options.headless = headless
        if headless:
            options.add_argument('--disable-gpu')
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.buttons = Buttons(browser=self.driver)
        self.html = None

    def open_page(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def get_page_html(self):
        return self.driver.page_source


    def maximize_window(self):
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()



import asyncio

class AsyncHeadlessChromeDriver:
    def __init__(self, driver_path: str = '/usr/local/bin/chromedriver', headless: bool = True):
        options = Options()
        options.headless = headless
        if headless:
            options.add_argument('--disable-gpu')
        service = Service(executable_path=driver_path)
        self.driver = None
        self.service = service
        self.options = options
        self.buttons = None
        self.html = None

    async def open_page(self, url):
        if not self.driver:
            self.driver = await asyncio.to_thread(webdriver.Chrome, service=self.service, options=self.options)
            self.buttons = Buttons(browser=self.driver)
        await asyncio.to_thread(self.driver.execute_script, 'window.open()')
        await asyncio.to_thread(self.driver.switch_to.window, self.driver.window_handles[-1])
        await asyncio.to_thread(self.driver.get, url)

    def get_page_html(self):
        return self.driver.page_source

    def maximize_window(self):
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()
        self.driver = None
        self.buttons = None
