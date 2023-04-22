from datetime import datetime


def get_today_date() -> str:
    today = datetime.today()
    return today.strftime("%d.%m")
