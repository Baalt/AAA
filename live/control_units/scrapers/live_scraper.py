import re
import time
from bs4 import BeautifulSoup
from typing import Dict

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class FootballParser:
    def __init__(self, driver, match_dct: Dict[str, Dict[str, str]]):
        self.driver = driver
        self.match_dct = match_dct
        self.container = None  # Будет найден в _parse_with_auto_scroll
        self._parse_with_auto_scroll()
        self._clean_matches()  # Очистка сразу после парсинга

    def _get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.get_page_html(), 'lxml')

    def _parse_matches(self) -> int:
        soup = self._get_soup()
        event_divs = soup.find_all('div', class_=re.compile(r'^sport-base-event'))

        added = 0
        for event in event_divs:
            name_tag = event.find('a', class_=re.compile(r'sport-event__name'))
            if not name_tag:
                continue
            match_name = name_tag.get_text(strip=True)
            if not match_name or match_name in self.match_dct:
                continue

            factor_divs = event.find_all('div', class_=re.compile(r'^factor-value'))
            if len(factor_divs) < 3:
                continue

            try:
                odd_home_str = factor_divs[0].get_text(strip=True)
                odd_away_str = factor_divs[2].get_text(strip=True)
                odd_home = float(odd_home_str)
                odd_away = float(odd_away_str)
            except (ValueError, IndexError):
                continue

            entry = None
            if odd_home < 1.56:
                entry = {
                    'team1': f"leader {odd_home_str}",
                    'team2': f"underdog {odd_away_str}",
                    'status': True
                }
            elif odd_away < 1.56:
                entry = {
                    'team1': f"underdog {odd_home_str}",
                    'team2': f"leader {odd_away_str}",
                    'status': True
                }

            if entry:
                self.match_dct[match_name] = entry
                added += 1

        return added

    def _parse_with_auto_scroll(self):
        # Ждём загрузки страницы
        time.sleep(3)

        # Находим контейнер со скроллом
        self.container = self.driver.driver.find_element(
            By.CSS_SELECTOR, "div[tabindex='0'][class*='_vertical-overflow--']"
        )
        # print("Контейнер скролла найден. Начинаем постепенный парсинг...")

        # Начальный парсинг (верх страницы)
        added = self._parse_matches()
        # print(f"Начальный парсинг: добавлено {added} матчей")

        step = 0
        no_new_counter = 0  # Счётчик шагов без новых матчей

        while True:
            step += 1
            # print(f"\n--- Шаг скролла {step} ---")

            # Текущие размеры контейнера
            visible_height = self.driver.driver.execute_script(
                "return arguments[0].clientHeight", self.container
            )
            current_top = self.driver.driver.execute_script(
                "return arguments[0].scrollTop", self.container
            )
            total_height = self.driver.driver.execute_script(
                "return arguments[0].scrollHeight", self.container
            )

            # print(f"   scrollTop: {current_top} / scrollHeight: {total_height} (видимая высота: {visible_height})")

            # Скроллим вниз ровно на один видимый экран
            self.driver.driver.execute_script(
                "arguments[0].scrollTop += arguments[0].clientHeight;", self.container
            )

            # Пауза на подгрузку
            time.sleep(2)

            # Парсим новые матчи
            added = self._parse_matches()
            events_now = len(self.driver.driver.find_elements(By.CSS_SELECTOR, ".sport-base-event--W4qkO"))
            # print(f"   Добавлено новых матчей: {added}")
            # print(f"   Всего видимых событий на экране: {events_now}")
            # print(f"   Всего в словаре: {len(self.match_dct)}")

            # Проверка на конец списка
            new_top = self.driver.driver.execute_script(
                "return arguments[0].scrollTop", self.container
            )
            if new_top == current_top:  # Скролл не сдвинулся
                # print("Скролл достиг конца списка.")
                break

            # Защита от бесконечного цикла
            if added == 0:
                no_new_counter += 1
                if no_new_counter >= 5:
                    # print("Несколько шагов без новых матчей — завершаем скролл.")
                    break
            else:
                no_new_counter = 0

        # Финальный парсинг
        final_added = self._parse_matches()
        # print(f"\nФинальный проход: добавлено {final_added} матчей")
        # print(f"Итого собрано подходящих матчей: {len(self.match_dct)}")

        # МГНОВЕННЫЙ ВОЗВРАТ СКРОЛЛА НА САМЫЙ ВЕРХ
        # print("Возвращаем скролл мгновенно в самое начало...")
        self.driver.driver.execute_script("arguments[0].scrollTop = 0;", self.container)

        # print("Парсинг и возврат скролла завершены!")

    def _clean_matches(self):
        """Удаляет матчи с '(' в названии и заглушку 'Home — Away'"""
        keys_to_remove = [
            key for key in self.match_dct
            if '(' in key or key in ['Home — Away', 'Хозяева — Гости']
        ]
        for key in keys_to_remove:
            del self.match_dct[key]
        # print(f"Очистка завершена. Удалено {len(keys_to_remove)} записей. Осталось: {len(self.match_dct)}")

    def get_matches(self) -> Dict[str, Dict[str, str]]:
        return self.match_dct


class LiveFootballParser:
    def __init__(self, driver, strong_favorites: Dict[str, Dict[str, str]]):
        self.driver = driver
        self.strong_favorites = strong_favorites
        self.live_matches: Dict[str, Dict[str, str]] = {}
        self.container = None
        self._parse_with_auto_scroll()
        self._clean_matches()
        # Возврат наверх в конце
        if self.container:
            self.driver.driver.execute_script("arguments[0].scrollTop = 0;", self.container)
            time.sleep(3)
            # print("Live: Скролл возвращён наверх")

    def _get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.get_page_html(), 'lxml')

    def _parse_live_matches(self):
        soup = self._get_soup()
        event_wraps = soup.find_all('div', class_=re.compile(r'^sport-base-event-wrap'))

        updated = 0
        for wrap in event_wraps:
            name_tag = wrap.find('a', class_=re.compile(r'sport-event__name'))
            if not name_tag:
                continue
            match_name = name_tag.get_text(strip=True)
            if not match_name:
                continue

            # Время матча (класс обычно event-block-current-time__value или содержащий event-block-current-time)
            time_span = wrap.find('span', class_=re.compile(r'event-block-current-time__time--'))
            current_time = time_span.get_text(strip=True) if time_span else "N/A"

            # Счёт (класс обычно event-block-score__value или содержащий event-block-score)
            score_span = wrap.find('span', class_=re.compile(r'event-block-score'))
            current_score = score_span.get_text(strip=True) if score_span else "?:?"

            if match_name not in self.live_matches:
                updated += 1

            self.live_matches[match_name] = {
                "time": current_time,
                "score": current_score
            }

        return updated

    def _parse_with_auto_scroll(self):
        try:
            # Универсальный поиск: div с классом начинающимся на virtual-list-
            virtual_list = self.driver.driver.find_element(
                By.CSS_SELECTOR, "div[class^='virtual-list--']"
            )
            # print(f"Live: Найден virtual-list с классами: {virtual_list.get_attribute('class')}")

            # Скроллящийся контейнер — родитель с tabindex="0"
            self.container = virtual_list.find_element(By.XPATH, "./..")  # parent
            if self.container.get_attribute("tabindex") != "0":
                # Fallback: ищем ближайший tabindex="0" вверх
                self.container = self.driver.driver.find_element(
                    By.CSS_SELECTOR, "div[tabindex='0'][class*='_vertical-overflow--']"
                )
            # print("Live: Контейнер скролла найден успешно.")
        except NoSuchElementException as e:
            print("Ошибка: Не удалось найти контейнер скролла в live.")
            print(e)
            # Дополнительный fallback: тот же, что в прематче
            try:
                self.container = self.driver.driver.find_element(
                    By.CSS_SELECTOR, "div[tabindex='0'][class*='_vertical-overflow--']"
                )
                print("Live: Использован fallback-селектор из прематча.")
            except:
                print("Live: Полный фейл поиска контейнера. Парсинг без скролла.")
                self._parse_live_matches()  # Хотя бы начальный парсинг
                return

        # Начальный парсинг
        self._parse_live_matches()
        # print(f"Live: Начальный парсинг — {len(self.live_matches)} матчей")

        step = 0
        no_new_counter = 0

        while True:
            step += 1
            # print(f"\n--- Live: Шаг скролла {step} ---")

            current_top = self.driver.driver.execute_script("return arguments[0].scrollTop", self.container)
            # total_height = self.driver.driver.execute_script("return arguments[0].scrollHeight", self.container)
            # print(f"   scrollTop: {current_top} / scrollHeight: {total_height}")

            # Скролл на один экран
            self.driver.driver.execute_script(
                "arguments[0].scrollTop += arguments[0].clientHeight;", self.container
            )

            time.sleep(2)

            updated = self._parse_live_matches()
            # print(f"   Обновлено/добавлено: {updated}")
            # print(f"   Всего live-матчей: {len(self.live_matches)}")

            # Печать словаря
            # print("\nТекущие live-матчи:")
            # for name, data in self.live_matches.items():
            #     print(f"   {name} | Время: {data['time']} | Счёт: {data['score']}")

            # Конец списка
            new_top = self.driver.driver.execute_script("return arguments[0].scrollTop", self.container)
            if new_top == current_top:
                # print("Live: Конец списка достигнут.")
                break

            if updated == 0:
                no_new_counter += 1
                if no_new_counter >= 4:
                    # print("Live: Нет новых матчей несколько шагов — стоп.")
                    break
            else:
                no_new_counter = 0

        # print(f"\nLive-парсинг завершён. Всего: {len(self.live_matches)} матчей")

    def _clean_matches(self):
        """Удаляет матчи с '(' в названии и с возрастными категориями типа U20, U21 и т.п."""
        keys_to_remove = [
            key for key in self.live_matches
            if '(' in key or re.search(r'U\d{2}', key)
        ]
        for key in keys_to_remove:
            del self.live_matches[key]
        # print(f"Очистка завершена. Удалено {len(keys_to_remove)} записей. Осталось: {len(self.match_dct)}")

    def get_live_matches(self) -> Dict[str, Dict[str, str]]:
        return self.live_matches
