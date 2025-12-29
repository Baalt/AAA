import subprocess
import time


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
            f"⚠️ ТОЧКА ВХОДА!\n\n"
            f"Матч: {self.match_name}\n"
            f"💰 {self.team1_label} - {self.team2_label}"
            f"⏱ Время: {self.time} | Счёт: {self.score}\n"
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

        for match_name, live_data in self.live_matches.items():
            if match_name not in self.strong_favorites:
                continue

            self.matches_found += 1
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
            favorite_winning_or_draw = favorite_goals >= underdog_goals

            current_status = fav_data.get('status', True)

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
                await self.telegram.send_message_with_files(message)

                self.play_loud_alert_mac(count=8, volume=25)
                print(message)
                print("-" * 40)


                # Выключаем статус — сохраняется в оригинальном словаре!
                fav_data['status'] = False

            elif favorite_winning_or_draw and not current_status:
                # Фаворит восстановился — снова активируем на будущее
                fav_data['status'] = True

        # Итог
        return self.matches_found


    def play_loud_alert_mac(self, count=8, volume=20):
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
