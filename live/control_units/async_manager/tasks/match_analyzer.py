import asyncio

from async_live.control_units.browser.browser import AsyncHeadlessChromeDriver


class BrowserController:
    def __init__(self):
        self.driver = AsyncHeadlessChromeDriver()

    async def open_three_urls(self, urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(self.driver.open_page(url)))
        await asyncio.gather(*tasks)

    def close_browser(self):
        self.driver.close()


controller = BrowserController()
urls = ['https://www.google.com', 'https://www.python.org', 'https://www.amazon.com']
asyncio.run(controller.open_three_urls(urls))
input()
controller.close_browser()
