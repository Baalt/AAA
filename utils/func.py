import re
from datetime import datetime, timedelta


def get_today_date() -> str:
    today = datetime.today()
    return today.strftime("%d.%m")


def get_tomorrow_date() -> str:
    tomorrow = datetime.today() + timedelta(days=1)
    return tomorrow.strftime("%d.%m")


def is_valid_name(name):
    return '(' not in name and '-pro' not in name and not re.search('U\d\d', name)

