from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser.button_box import Buttons


class LiveChromeDriver:
    def __init__(self, driver_path: str = '/usr/local/bin/chromedriver', headless: bool = False):
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


class SmartChromeDriver(LiveChromeDriver):
    def login(self, username, password):
        # Wait up to 10 seconds for the email and password input fields to appear
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        # Fill in the email and password fields
        email_field.send_keys(username)
        password_field.send_keys(password)

        # Find and click the login button
        login_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//button[normalize-space(text())="Войти"]')))
        login_button.click()
