import re
import math
from datetime import datetime, timedelta


def get_today_date() -> str:
    today = datetime.today()
    return today.strftime("%d.%m")


def get_tomorrow_date() -> str:
    tomorrow = datetime.today() + timedelta(days=1)
    return tomorrow.strftime("%d.%m")


def is_valid_name(name):
    return '(' not in name and '-pro' not in name and not re.search('U\d\d', name)


def custom_round(number, tenths=0.35):
    if number - math.floor(number) >= tenths:
        return math.ceil(number)
    else:
        return math.floor(number)
