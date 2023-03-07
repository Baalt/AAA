import asyncio

from browser.browser import HeadlessChromeDriver


class MultipleTabsOpener:
    def __init__(self, driver: HeadlessChromeDriver, smart_dict):
        self.driver = driver
        self.driver.maximize_window()
        self.smart_dict = smart_dict

    async def open_all_urls(self, browser_preparer):
        tabs = list(self.smart_dict.keys())
        main_tab = tabs[0]
        self.driver.open_page(self.smart_dict[main_tab]['url'])
        browser_preparer(driver=self.driver).switch_language()
        tasks = []
        for tab in tabs[1:]:
            script = "window.open('{}', '_blank');".format(self.smart_dict[tab]['url'])
            task = asyncio.create_task(self.execute_script_async(script))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def execute_script_async(self, script):
        await asyncio.to_thread(self.driver.driver.execute_script, script)

    def get_driver(self):
        return self.driver
