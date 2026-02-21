import subprocess
import time
import re

import telegram.error


class LosingFavoriteMessage:
    def __init__(self, match_name: str, live_data: dict, fav_data: dict,
                 goals_team1: int, goals_team2: int):
        self.match_name = match_name
        self.time = live_data['time']
        self.score = live_data['score']
        self.team1_label = fav_data['team1']  # например: "leader 1.25"
        self.team2_label = fav_data['team2']  # например: "underdog 11.00"
        self.goals_team1 = goals_team1
        self.goals_team2 = goals_team2

    def format(self) -> str:
        # Строка с коэффициентами и ролями: именно как ты хочешь
        message = (
            f"⚠️ ТОЧКА ВХОДА!\n"
            f"Матч: {self.match_name}\n"
            f"💰 {self.team1_label} - {self.team2_label}\n"
            f"⏱ Время: {self.time} | Счёт: {self.score}\n"
        )
        return message


class WeakerLosingMessage:
    def __init__(self, match_name: str, live_data: dict, fav_data: dict, condition: int,
                 second_corners: int, second_shots: int):
        self.match_name = match_name
        self.time = live_data['time']
        self.score = live_data['score']
        self.team1_label = fav_data['team1']
        self.team2_label = fav_data['team2']
        self.condition = condition
        self.second_corners = second_corners
        self.second_shots = second_shots

    def format(self) -> str:
        message = (
            f"⚠️ ТОЧКА ВХОДА WEAKER! Условие {self.condition}\n"
            f"Матч: {self.match_name}\n"
            f"💰 {self.team1_label} - {self.team2_label}\n"
            f"⏱ Время: {self.time} | Счёт: {self.score}\n"
            f"Угловые 2-й тайм: {self.second_corners} | Удары в створ 2-й тайм: {self.second_shots}\n"
        )
        return message


class MatchChecker:
    def __init__(self, strong_favorites: dict, live_matches: dict, tel):
        self.strong_favorites = strong_favorites  # Работаем с оригинальным словарём
        self.live_matches = live_matches
        self.telegram = tel
        self.matches_found = 0

    async def check_matches(self):
        self.matches_found = 0
        matched_list = []

        for match_name, live_data in self.live_matches.items():
            if match_name not in self.strong_favorites:
                continue
            # print(match_name, self.strong_favorites[match_name])
            self.matches_found += 1
            matched_list.append(match_name)
            fav_data = self.strong_favorites[match_name]

            # Определяем, кто фаворит
            if 'leader' in fav_data['team1']:
                favorite_is_team1 = True
            elif 'leader' in fav_data['team2']:
                favorite_is_team1 = False
            else:
                continue

            score = live_data['score']

            try:
                goals_team1, goals_team2 = map(int, score.split(':'))
            except:
                continue

            # Голы фаворита и андердога
            favorite_goals = goals_team1 if favorite_is_team1 else goals_team2
            underdog_goals = goals_team2 if favorite_is_team1 else goals_team1

            favorite_losing = favorite_goals < underdog_goals
            # favorite_losing_by_two = (underdog_goals - favorite_goals == 2)
            favorite_winning_or_draw = favorite_goals >= underdog_goals

            current_status = fav_data.get('status', True)
            # current_goal_status = fav_data.get('status_goal', True)

            if favorite_losing and current_status:
                # Только что фаворит начал проигрывать — отправляем сигнал
                msg_builder = LosingFavoriteMessage(
                    match_name=match_name,
                    live_data=live_data,
                    fav_data=fav_data,
                    goals_team1=goals_team1,
                    goals_team2=goals_team2
                )
                message = msg_builder.format()
                self.play_loud_alert_mac(count=3, volume=25)
                print(message)
                print("-" * 40)
                fav_data['status'] = False
                try:
                    await self.telegram.send_message_with_files(message)
                except telegram.error.NetworkError:
                    print('Ошибка отправки сообщения в telegram')
                # Выключаем статус — сохраняется в оригинальном словаре!

            if favorite_winning_or_draw and not current_status:
                # Фаворит восстановился — снова активируем на будущее
                fav_data['status'] = True

        return self.matches_found, matched_list

    def play_loud_alert_mac(self, count=8, volume=1):
        loud_sounds = [
            '/System/Library/Sounds/Sosumi.aiff',  # классический "ошибка"
            '/System/Library/Sounds/Submarine.aiff',  # подводная лодка — громкий!
            '/System/Library/Sounds/Funk.aiff',  # фанковый сигнал
            '/System/Library/Sounds/Purr.aiff',  # рычание
            '/System/Library/Sounds/Glass.aiff',  # стекло
            '/System/Library/Sounds/Basso.aiff'  # басовый
        ]

        for i in range(count):
            sound = loud_sounds[i % len(loud_sounds)]
            subprocess.Popen(['afplay', '-v', str(volume), sound])
            time.sleep(0.35)


class WeakerMatchChecker:
    def __init__(self, weaker_favorites: dict, live_matches: dict, tel):
        self.weaker_favorites = weaker_favorites
        self.live_matches = live_matches
        self.telegram = tel
        self.matches_found = 0

    async def check_matches(self):
        self.matches_found = 0
        matched_list = []

        for match_name, live_data in self.live_matches.items():
            if match_name not in self.weaker_favorites:
                continue
            fav_data = self.weaker_favorites[match_name]

            # Определяем, кто фаворит
            if 'leader' in fav_data['team1']:
                favorite_is_team1 = True
            elif 'leader' in fav_data['team2']:
                favorite_is_team1 = False
            else:
                continue

            score = live_data['score']
            try:
                goals_team1, goals_team2 = map(int, score.split(':'))
            except:
                continue

            favorite_goals = goals_team1 if favorite_is_team1 else goals_team2
            underdog_goals = goals_team2 if favorite_is_team1 else goals_team1

            draw = favorite_goals == underdog_goals
            leader_leads = favorite_goals > underdog_goals

            time_str = live_data['time']
            time_match = re.search(r'\d+', time_str)
            if not time_match:
                continue
            time_min = int(time_match.group())
            if time_min <= 45:
                continue

            stats = live_data.get('stats', {})
            if 'угловые' not in stats and 'удары в створ' not in stats:
                continue

            corners = stats.get('угловые', {})
            shots = stats.get('удары в створ', {})
            if not corners.get('first_half') and not shots.get('first_half'):
                continue

            total_first_corners = 0
            total_first_shots = 0
            first_corners_t1 = first_corners_t2 = 0
            first_shots_t1 = first_shots_t2 = 0

            try:
                if corners.get('first_half'):
                    first_corners_t1, first_corners_t2 = map(int, re.search(r'\((\d+)-(\d+)\)', corners['first_half']).groups())
                    total_first_corners = first_corners_t1 + first_corners_t2
                if shots.get('first_half'):
                    first_shots_t1, first_shots_t2 = map(int, re.search(r'\((\d+)-(\d+)\)', shots['first_half']).groups())
                    total_first_shots = first_shots_t1 + first_shots_t2
            except:
                continue

            state_key = 'weaker_state'
            if state_key not in fav_data:
                fav_data[state_key] = {
                    'first_set': False,
                    'tracked_corners': False,
                    'tracked_shots': False,
                    'sent1': False,
                    'sent2': False,
                    'sent3': False,
                    'last_second_total_corners': 0,
                    'last_second_total_shots': 0,
                    'last_favorite_goals': 0,
                    'last_time': 0
                }
            state = fav_data[state_key]

            if not state['first_set']:
                state['first_corners_t1'] = first_corners_t1
                state['first_corners_t2'] = first_corners_t2
                state['first_shots_t1'] = first_shots_t1
                state['first_shots_t2'] = first_shots_t2
                state['tracked_corners'] = total_first_corners > 5
                state['tracked_shots'] = total_first_shots > 5
                state['first_set'] = True
                state['last_favorite_goals'] = favorite_goals
                state['last_time'] = time_min

            if not state['tracked_corners'] and not state['tracked_shots']:
                continue

            # Теперь добавляем в счёт и список, поскольку матч tracked
            self.matches_found += 1
            matched_list.append(match_name)

            if time_min >= 64:
                continue  # Прекращаем отслеживание после 63 минуты

            try:
                second_total_corners = 0
                second_total_shots = 0
                if 'угловые' in stats:
                    current_corners_t1, current_corners_t2 = map(int, corners['current'].split(':'))
                    second_corners_t1 = max(0, current_corners_t1 - state['first_corners_t1'])
                    second_corners_t2 = max(0, current_corners_t2 - state['first_corners_t2'])
                    second_total_corners = second_corners_t1 + second_corners_t2
                if 'удары в створ' in stats:
                    current_shots_t1, current_shots_t2 = map(int, shots['current'].split(':'))
                    second_shots_t1 = max(0, current_shots_t1 - state['first_shots_t1'])
                    second_shots_t2 = max(0, current_shots_t2 - state['first_shots_t2'])
                    second_total_shots = second_shots_t1 + second_shots_t2
            except:
                continue

            if time_min <= state['last_time']:
                continue

            # Условие 1
            if (draw or leader_leads) and time_min <= 55 and not state['sent1']:
                corners_reached = state['tracked_corners'] and (second_total_corners >= 5 and state['last_second_total_corners'] < 5)
                shots_reached = state['tracked_shots'] and (second_total_shots >= 4 and state['last_second_total_shots'] < 4)
                if corners_reached or shots_reached:
                    msg_builder = WeakerLosingMessage(
                        match_name=match_name,
                        live_data=live_data,
                        fav_data=fav_data,
                        condition=1,
                        second_corners=second_total_corners,
                        second_shots=second_total_shots
                    )
                    message = msg_builder.format()
                    self.play_loud_alert_mac(count=3, volume=25)
                    print(message)
                    print("-" * 40)
                    try:
                        await self.telegram.send_message_with_files(message)
                    except telegram.error.NetworkError:
                        print('Ошибка отправки сообщения в telegram')
                    state['sent1'] = True

            # Условие 2
            if time_min > 55 and time_min <= 63 and (draw or leader_leads) and not state['sent2']:
                corners_trigger = state['tracked_corners'] and (second_total_corners >= 4) and (second_total_corners > state['last_second_total_corners'])
                shots_trigger = state['tracked_shots'] and (second_total_shots >= 4) and (second_total_shots > state['last_second_total_shots'])
                if corners_trigger or shots_trigger:
                    msg_builder = WeakerLosingMessage(
                        match_name=match_name,
                        live_data=live_data,
                        fav_data=fav_data,
                        condition=2,
                        second_corners=second_total_corners,
                        second_shots=second_total_shots
                    )
                    message = msg_builder.format()
                    self.play_loud_alert_mac(count=3, volume=25)
                    print(message)
                    print("-" * 40)
                    try:
                        await self.telegram.send_message_with_files(message)
                    except telegram.error.NetworkError:
                        print('Ошибка отправки сообщения в telegram')
                    state['sent2'] = True

            # Условие 3
            if time_min <= 63 and (draw or leader_leads) and not state['sent3']:
                corners_ok = state['tracked_corners'] and second_total_corners >= 3
                shots_ok = state['tracked_shots'] and second_total_shots >= 2
                goal_scored = favorite_goals > state['last_favorite_goals']
                if (corners_ok or shots_ok) and goal_scored:
                    msg_builder = WeakerLosingMessage(
                        match_name=match_name,
                        live_data=live_data,
                        fav_data=fav_data,
                        condition=3,
                        second_corners=second_total_corners,
                        second_shots=second_total_shots
                    )
                    message = msg_builder.format()
                    self.play_loud_alert_mac(count=3, volume=25)
                    print(message)
                    print("-" * 40)
                    try:
                        await self.telegram.send_message_with_files(message)
                    except telegram.error.NetworkError:
                        print('Ошибка отправки сообщения в telegram')
                    state['sent3'] = True

            # Обновление last
            if state['tracked_corners']:
                state['last_second_total_corners'] = second_total_corners
            if state['tracked_shots']:
                state['last_second_total_shots'] = second_total_shots
            state['last_favorite_goals'] = favorite_goals
            state['last_time'] = time_min

        return self.matches_found, matched_list

    def play_loud_alert_mac(self, count=8, volume=1):
        loud_sounds = [
            '/System/Library/Sounds/Sosumi.aiff',
            '/System/Library/Sounds/Submarine.aiff',
            '/System/Library/Sounds/Funk.aiff',
            '/System/Library/Sounds/Purr.aiff',
            '/System/Library/Sounds/Glass.aiff',
            '/System/Library/Sounds/Basso.aiff'
        ]

        for i in range(count):
            sound = loud_sounds[i % len(loud_sounds)]
            subprocess.Popen(['afplay', '-v', str(volume), sound])
            time.sleep(0.35)
