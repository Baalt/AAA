import re
import time
from bs4 import BeautifulSoup
from typing import Dict

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class FootballParser:
    def __init__(self, driver, strong_favorites: Dict[str, Dict[str, str]],
                 weaker_favorites: Dict[str, Dict[str, str]]):
        self.driver = driver
        self.strong_favorites = strong_favorites  # Сильные фавориты: < 1.55
        self.weaker_favorites = weaker_favorites  # Слабые фавориты: >= 1.55
        self.container = None  # Будет найден в _parse_with_auto_scroll
        self._parse_with_auto_scroll()
        self._clean_matches()  # Очистка сразу после парсинга (для обоих)

    def _get_soup(self) -> BeautifulSoup:
        """Получает HTML страницы и парсит в BeautifulSoup."""
        return BeautifulSoup(self.driver.get_page_html(), 'lxml')

    def _parse_matches(self) -> int:
        """Парсит матчи и заполняет Оба словаря (strong + weaker)."""
        soup = self._get_soup()
        event_divs = soup.find_all('div', class_=re.compile(r'^sport-base-event'))

        added_strong = 0
        added_weaker = 0

        for event in event_divs:
            name_tag = event.find('a', class_=re.compile(r'sport-event__name'))
            if not name_tag:
                continue
            match_name = name_tag.get_text(strip=True)
            if not match_name:
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

            min_odd = min(odd_home, odd_away)

            # === STRONG FAVORITES: сильные фавориты < 1.55 ===
            if min_odd < 1.55 and match_name not in self.strong_favorites:
                if odd_home < odd_away:  # Home — фаворит
                    entry = {
                        'team1': f"leader {odd_home_str}",
                        'team2': f"underdog {odd_away_str}",
                        'status': True
                    }
                else:  # Away — фаворит
                    entry = {
                        'team1': f"underdog {odd_home_str}",
                        'team2': f"leader {odd_away_str}",
                        'status': True
                    }
                self.strong_favorites[match_name] = entry
                added_strong += 1

            # === WEAKER FAVORITES: слабые фавориты >= 1.55 ===
            if min_odd >= 1.55 and match_name not in self.weaker_favorites:
                if odd_home < odd_away:  # Home — фаворит
                    entry = {
                        'team1': f"leader {odd_home_str}",
                        'team2': f"underdog {odd_away_str}",
                        'status': True
                    }
                else:  # Away — фаворит
                    entry = {
                        'team1': f"underdog {odd_home_str}",
                        'team2': f"leader {odd_away_str}",
                        'status': True
                    }
                self.weaker_favorites[match_name] = entry
                added_weaker += 1

        return added_strong  # Для совместимости

    def _parse_with_auto_scroll(self):
        """Автоскролл и парсинг (как в оригинале)."""
        # Ждём загрузки страницы
        time.sleep(3)

        # Находим контейнер со скроллом (с fallback)
        try:
            self.container = self.driver.driver.find_element(
                By.CSS_SELECTOR, "div[tabindex='0'][class*='_vertical-overflow--']"
            )
        except NoSuchElementException:
            self._parse_matches()
            return

        # Начальный парсинг (верх страницы)
        added = self._parse_matches()

        step = 0
        no_new_counter = 0  # Счётчик шагов без новых матчей

        while True:
            step += 1

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

            # Скроллим вниз ровно на один видимый экран
            self.driver.driver.execute_script(
                "arguments[0].scrollTop += arguments[0].clientHeight;", self.container
            )

            # Пауза на подгрузку
            time.sleep(2)

            # Парсим новые матчи
            added = self._parse_matches()
            events_now = len(self.driver.driver.find_elements(By.CSS_SELECTOR, ".sport-base-event--W4qkO"))

            # Проверка на конец списка
            new_top = self.driver.driver.execute_script(
                "return arguments[0].scrollTop", self.container
            )
            if new_top == current_top:  # Скролл не сдвинулся
                break

            # Защита от бесконечного цикла
            if added == 0:
                no_new_counter += 1
                if no_new_counter >= 5:
                    break
            else:
                no_new_counter = 0

        # Финальный парсинг
        final_added = self._parse_matches()

        # МГНОВЕННЫЙ ВОЗВРАТ СКРОЛЛА НА САМЫЙ ВЕРХ
        self.driver.driver.execute_script("arguments[0].scrollTop = 0;", self.container)

    def _clean_matches(self):
        """Удаляет матчи с '(' в названии, заглушку 'Home — Away' и юношеские (U19, U18 и т.д.) для ОБОИХ словарей."""
        for favorites_dct in [self.strong_favorites, self.weaker_favorites]:
            keys_to_remove = [
                key for key in favorites_dct
                if '(' in key
                   or key in ['Home — Away', 'Хозяева — Гости']
                   or re.search(r'U\d{2}', key)
            ]
            for key in keys_to_remove:
                if key in favorites_dct:  # Защита
                    del favorites_dct[key]

    def get_matches(self) -> Dict[str, Dict[str, str]]:
        """Возвращает strong_favorites (для совместимости)."""
        return self.strong_favorites

    def get_weaker_matches(self) -> Dict[str, Dict[str, str]]:
        """Новый метод: возвращает weaker_favorites (фавориты >=1.55)."""
        return self.weaker_favorites


class LiveFootballParser:
    def __init__(self, driver):
        self.driver = driver
        self.live_matches: Dict[str, Dict[str, str]] = {}
        self.container = None
        self._parse_with_auto_scroll()
        self._clean_matches()
        # Возврат наверх в конце
        if self.container:
            self.driver.driver.execute_script("arguments[0].scrollTop = 0;", self.container)
            time.sleep(5)
            # print("Live: Скролл возвращён наверх")

    def _get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.get_page_html(), 'lxml')

    def _expand_more_stats(self):
        """Находит и кликает на кнопки 'Показать еще' для раскрытия статистики."""
        try:
            buttons = self.driver.driver.find_elements(By.CSS_SELECTOR, "div[class^='sport-show-more__caption']")
            for button in buttons:
                text = button.text.strip().lower()
                if text.startswith("показать еще"):
                    button.click()
                    time.sleep(1)  # Пауза на подгрузку
        except Exception as e:
            pass
            # print(f"Ошибка при раскрытии статистики: {e}")

    def _parse_live_matches(self):
        self._expand_more_stats()  # Раскрываем перед парсингом
        soup = self._get_soup()
        all_wraps = soup.find_all('div', class_=re.compile(r'^sport-base-event-wrap'))

        stats_keywords = {'угловые', 'удары в створ', 'вброс аутов'}

        updated = 0
        i = 0
        while i < len(all_wraps):
            wrap = all_wraps[i]
            name_tag = wrap.find('a', class_=re.compile(r'sport-event__name'))
            if not name_tag:
                i += 1
                continue
            match_name = name_tag.get_text(strip=True)
            if not match_name:
                i += 1
                continue

            # Время матча
            time_span = wrap.find('span', class_=re.compile(r'event-block-current-time__time--'))
            current_time = time_span.get_text(strip=True) if time_span else "N/A"

            # Счёт
            score_span = wrap.find('span', class_=re.compile(r'event-block-score'))
            current_score = score_span.get_text(strip=True) if score_span else "?:?"

            # Сбор статистики из этого и следующих wraps
            found_stats = set()
            stats_dict = {}

            # Проверка текущего wrap (редко, но на всякий)
            texts = wrap.find_all('div', class_=re.compile(r'^table-component-text'))
            for text_div in texts:
                text = text_div.get_text(strip=True).lower()
                if text in stats_keywords:
                    found_stats.add(text)
                    score_span_stat = wrap.find('span', class_=re.compile(r'^event-block-score'))
                    current = score_span_stat.get_text(strip=True) if score_span_stat else None
                    comment_div = wrap.find('div', class_=re.compile(r'^event-block-comment'))
                    first_half = comment_div.get_text(strip=True) if comment_div else None
                    stats_dict[text] = {'current': current, 'first_half': first_half}

            # Проверка следующих wraps
            j = i + 1
            while j < len(all_wraps):
                next_wrap = all_wraps[j]
                next_name_tag = next_wrap.find('a', class_=re.compile(r'sport-event__name'))
                if next_name_tag:
                    break

                next_texts = next_wrap.find_all('div', class_=re.compile(r'^table-component-text'))
                for text_div in next_texts:
                    text = text_div.get_text(strip=True).lower()
                    if text in stats_keywords:
                        found_stats.add(text)
                        score_span_stat = next_wrap.find('span', class_=re.compile(r'^event-block-score'))
                        current = score_span_stat.get_text(strip=True) if score_span_stat else None
                        comment_div = next_wrap.find('div', class_=re.compile(r'^event-block-comment'))
                        first_half = comment_div.get_text(strip=True) if comment_div else None
                        stats_dict[text] = {'current': current, 'first_half': first_half}

                j += 1

            # Если найдена статистика, добавляем матч
            if len(found_stats) > 0:
                if match_name not in self.live_matches:
                    updated += 1
                self.live_matches[match_name] = {
                    "time": current_time,
                    "score": current_score,
                    "stats": stats_dict
                }

            i = j

        return updated

    def _parse_with_auto_scroll(self):
        """Улучшенный поиск контейнера для live (с несколькими fallback)."""
        try:
            # Основной: virtual-list
            virtual_list = self.driver.driver.find_element(
                By.CSS_SELECTOR, "div[class^='virtual-list--']"
            )
            self.container = virtual_list.find_element(By.XPATH, "./..")
            if self.container.get_attribute("tabindex") != "0":
                raise NoSuchElementException("Не tabindex=0")
            # print("Live: Контейнер virtual-list найден.")
        except NoSuchElementException:
            try:
                # Fallback 1: vertical-overflow (как в прематче)
                self.container = self.driver.driver.find_element(
                    By.CSS_SELECTOR, "div[tabindex='0'][class*='_vertical-overflow--']"
                )
                # print("Live: Fallback 1 — vertical-overflow найден.")
            except NoSuchElementException:
                try:
                    # Fallback 2: Более общий селектор (любая вертикальная прокрутка)
                    self.container = self.driver.driver.find_element(
                        By.CSS_SELECTOR, "div[class*='overflow'][tabindex='0']"
                    )
                    print("Live: Fallback 2 — общий overflow найден.")
                except NoSuchElementException:
                    print("Live: Полный фейл поиска контейнера. Парсинг без скролла.")
                    self._parse_live_matches()
                    return

        # Начальный парсинг с раскрытием
        self._parse_live_matches()

        step = 0
        no_new_counter = 0

        while True:
            step += 1

            current_top = self.driver.driver.execute_script("return arguments[0].scrollTop", self.container)

            # Скролл на один экран
            self.driver.driver.execute_script(
                "arguments[0].scrollTop += arguments[0].clientHeight;", self.container
            )

            time.sleep(2)

            # После скролла — раскрываем новые "Показать еще"
            self._expand_more_stats()

            updated = self._parse_live_matches()

            # Конец списка
            new_top = self.driver.driver.execute_script("return arguments[0].scrollTop", self.container)
            if new_top == current_top:
                break

            if updated == 0:
                no_new_counter += 1
                if no_new_counter >= 4:
                    break
            else:
                no_new_counter = 0

    def _clean_matches(self):
        """Очистка live-матчей."""
        keys_to_remove = [
            key for key in self.live_matches
            if '(' in key or re.search(r'U\d{2}', key)
        ]
        for key in keys_to_remove:
            del self.live_matches[key]

    def get_live_matches(self) -> Dict[str, Dict[str, str]]:
        return self.live_matches
