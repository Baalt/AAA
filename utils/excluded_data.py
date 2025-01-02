import os
import yaml

from utils.func import get_today_date


def get_excluded_data():
    file_path = f'data/{get_today_date()}_excluded_games.yaml'
    remove_old_excluded_files()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            excluded_games = yaml.safe_load(file) or {}
    else:
        excluded_games = {}
    return excluded_games


def remove_old_excluded_files():
    folder_path = "data"
    current_file_name = f"{get_today_date()}_excluded_games.yaml"

    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не существует.")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith("_excluded_games.yaml") and file_name != current_file_name:
            os.remove(file_path)
            print(f"Удален файл: {file_path}")


def save_or_update_excluded_data(excluded_games):
    file_path = f"data/{get_today_date()}_excluded_games.yaml"

    file_data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            file_data = yaml.safe_load(file) or {}

    if file_data != excluded_games:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(excluded_games, file, default_flow_style=False, allow_unicode=True)
