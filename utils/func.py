import os
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


def delete_files_in_folder(folder_path='graph/data'):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)


def get_matching_files(ordered_file_list, directory='graph/data'):
    all_files = os.listdir(directory)
    matching_files = [file for file in ordered_file_list if os.path.basename(file) in all_files]
    return matching_files
