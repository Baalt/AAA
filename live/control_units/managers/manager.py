from live.control_units.managers.automation_schedule import ScheduleManager
from live.control_units.managers.web_crawler import WebCrawler
from toolz.pickle_manager import PickleHandler


if __name__ == '__main__':
    smart_dict = PickleHandler().read_data()
    browser = ScheduleManager(smart_dict=smart_dict)
    full_smart_dict = browser.run()
    operator = WebCrawler(driver=browser.get_driver(), smart_data=full_smart_dict)
    operator.run_crawler()


