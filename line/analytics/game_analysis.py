import time

from telega import config
from telega.telegram_bot import TelegramBot
from graph.teams_stats_viz import TeamsStatsVisualizer
from utils.func import delete_files_in_folder, get_matching_files
from utils.stat_switcher import ordered_file_list


class GameStatAnalyzer:

    def __init__(self, lv_schedule: dict, lg_strct: dict, lg_data: dict):
        self.lv_schedule = lv_schedule
        self.lg_strct = lg_strct
        self.lg_data = lg_data
        self.tel = TelegramBot(token=config.token, chat_id=config.chat_id)

    async def run(self):
        flag = True
        for lg_dct in self.lv_schedule['data']:
            # if lg_dct['league'] == '':
            #     flag = True
            if flag:
                for game in lg_dct['match_data']:
                    await self.analyze(game['team1_name'],
                                       game['team2_name'],
                                       game['ref_name'],
                                       lg_dct['league'])

    async def analyze(self, team1_name, team2_name, ref_name, lg_key):
        try:
            lg_strct = self.lg_strct[lg_key]
        except KeyError:
            return

        message_lst = []
        stat_viz_set = set()

        position_up_25 = self.lg_strct[lg_key]['position']['more_25']
        position_down_25 = self.lg_strct[lg_key]['position']['less_25']

        for stat in lg_strct:
            if stat not in ['ref_yellow cards', 'ref_fouls', 'position']:
                more25 = self.lg_strct[lg_key][stat]['more_25']
                more15 = self.lg_strct[lg_key][stat]['more_15-25']
                less25 = self.lg_strct[lg_key][stat]['less_25']
                less15 = self.lg_strct[lg_key][stat]['less_15-25']

                if stat not in ['goals', 'yellow cards', 'fouls', 'throw-ins']:
                    if team1_name in more25 and team2_name in more25:
                        message_lst.append(f'STRONG_TOTAL_OVER_{stat}')
                        stat_viz_set.add(stat)
                    elif (team1_name in more25 and team2_name in more15) or (
                            team1_name in more15 and team2_name in more25):
                        message_lst.append(f'NORMAL_TOTAL_OVER_{stat}')
                        stat_viz_set.add(stat)

                    if team1_name in less25 and team2_name in less25:
                        message_lst.append(f'STRONG_TOTAL_UNDER_{stat}')
                        stat_viz_set.add(stat)

                    elif (team1_name in less25 and team2_name in less15) or (
                            team1_name in less15 and team2_name in less25):
                        message_lst.append(f'NORMAL_TOTAL_UNDER_{stat}')
                        stat_viz_set.add(stat)

                    if (team1_name in more25 and team2_name in less25) or (
                            team1_name in less25 and team2_name in more25):
                        message_lst.append(f'STRONG_HANDICAP_{stat}')
                        stat_viz_set.add(stat)
                    elif (team1_name in more25 and team2_name in less15) or (
                            team1_name in more15 and team2_name in less25):
                        message_lst.append(f'NORMAL_HANDICAP_{stat}')
                        stat_viz_set.add(stat)
                    elif (team1_name in less25 and team2_name in more15) or (
                            team1_name in less15 and team2_name in more25):
                        message_lst.append(f'NORMAL_HANDICAP_{stat}')
                        stat_viz_set.add(stat)

                    if team1_name in more25:
                        message_lst.append(f'IND_1_OVER_{stat}')
                        stat_viz_set.add(stat)
                    elif team1_name in less25:
                        message_lst.append(f'IND_1_UNDER_{stat}')
                        stat_viz_set.add(stat)

                    if team2_name in more25:
                        message_lst.append(f'IND_2_OVER_{stat}')
                        stat_viz_set.add(stat)
                    elif team2_name in less25:
                        message_lst.append(f'IND_2_UNDER_{stat}')
                        stat_viz_set.add(stat)

                elif stat in ['throw-ins', 'fouls']:
                    more = more25 + more15
                    less = less25 + less15

                    if stat == 'throw-ins':
                        if (team1_name in more and team1_name in position_up_25) and (
                                team2_name in less and team2_name in position_down_25):
                            message_lst.append(f'STRONG_HANDICAP_{stat}')
                            stat_viz_set.add(stat)

                        elif (team1_name in less and team1_name in position_down_25) and (
                                team2_name in more and team2_name in position_up_25):
                            message_lst.append(f'STRONG_HANDICAP_{stat}')
                            stat_viz_set.add(stat)

                        elif (team1_name in more and team2_name in less) or (team1_name in less and team2_name in more):
                            message_lst.append(f'HANDICAP_{stat}')
                            stat_viz_set.add(stat)

                        if team1_name in more and team2_name in more:
                            message_lst.append(f'TOTAL_OVER_{stat}')
                            stat_viz_set.add(stat)

                        if (team1_name in position_up_25 and team1_name in less and team2_name in position_down_25):
                            message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif (team2_name in position_up_25 and team2_name in less and team1_name in position_down_25):
                            message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif team1_name in less and team2_name in less:
                            message_lst.append(f'TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team1_name in more:
                            message_lst.append(f'IND_1_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team1_name in less:
                            message_lst.append(f'IND_1_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team2_name in more:
                            message_lst.append(f'IND_2_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team2_name in less:
                            message_lst.append(f'IND_2_UNDER_{stat}')
                            stat_viz_set.add(stat)

                    elif stat == 'fouls':
                        if (team1_name in more and team2_name in less) or (team1_name in less and team2_name in more):
                            message_lst.append(f'HANDICAP_{stat}')
                            stat_viz_set.add(stat)

                        if ref_name:
                            ref_stat = 'ref_' + stat
                            try:
                                ref_more25 = self.lg_strct[lg_key][ref_stat]['more_25']
                            except KeyError:
                                continue
                            ref_more15_25 = self.lg_strct[lg_key][ref_stat]['more_15-25']
                            ref_avg5_5 = self.lg_strct[lg_key][ref_stat]['avg_5-5']
                            ref_less25 = self.lg_strct[lg_key][ref_stat]['less_25']
                            ref_less15_25 = self.lg_strct[lg_key][ref_stat]['less_15-25']
                            ref_less5_15 = self.lg_strct[lg_key][ref_stat]['less_5-15']
                            ref_more = ref_more25 + ref_more15_25
                            ref_less5 = ref_less25 + ref_less15_25 + ref_less5_15
                            ref_avg = ref_less5 + ref_avg5_5

                            less5 = self.lg_strct[lg_key][stat]['less_5-15']
                            avg5_5 = self.lg_strct[lg_key][stat]['avg_5-5']
                            avg = less25 + less15 + less5 + avg5_5

                            if team1_name in more and team2_name in more and ref_name in ref_more:
                                message_lst.append(f'TOTAL_OVER_{stat}')
                                stat_viz_set.add(stat)

                            if team1_name in less and team2_name in less and ref_name in ref_less5:
                                message_lst.append(f'TOTAL_UNDER_{stat}')
                                stat_viz_set.add(stat)

                            elif (team1_name in position_up_25 and team1_name in avg) and (
                                    team2_name in position_down_25 and team2_name in avg) and ref_name in ref_avg:
                                message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                                stat_viz_set.add(stat)

                            elif (team1_name in position_down_25 and team1_name in avg) and (
                                    team2_name in position_up_25 and team2_name in avg) and ref_name in ref_avg:
                                message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                                stat_viz_set.add(stat)

                            if team1_name in more and ref_name in ref_more:
                                message_lst.append(f'IND_1_OVER_{stat}')
                                stat_viz_set.add(stat)
                            elif team1_name in less and ref_name in ref_less5:
                                message_lst.append(f'IND_1_UNDER_{stat}')
                                stat_viz_set.add(stat)

                            if team2_name in more and ref_name in ref_more:
                                message_lst.append(f'IND_2_OVER_{stat}')
                                stat_viz_set.add(stat)
                            elif team2_name in less and ref_name in ref_less5:
                                message_lst.append(f'IND_2_UNDER_{stat}')
                                stat_viz_set.add(stat)


                elif stat == 'yellow cards':
                    if (team1_name in more25 and team2_name in less25) or (
                            team1_name in less25 and team2_name in more25):
                        message_lst.append(f'STRONG_HANDICAP_{stat}')
                        stat_viz_set.add(stat)
                    elif (team1_name in more25 and team2_name in less15) or (
                            team1_name in more15 and team2_name in less25):
                        message_lst.append(f'NORMAL_HANDICAP_{stat}')
                        stat_viz_set.add(stat)
                    elif (team1_name in less25 and team2_name in more15) or (
                            team1_name in less15 and team2_name in more25):
                        message_lst.append(f'NORMAL_HANDICAP_{stat}')
                        stat_viz_set.add(stat)

                    if ref_name:
                        ref_stat = 'ref_' + stat
                        try:
                            ref_more25 = self.lg_strct[lg_key][ref_stat]['more_25']
                        except KeyError:
                            continue
                        ref_more15_25 = self.lg_strct[lg_key][ref_stat]['more_15-25']
                        ref_avg5_5 = self.lg_strct[lg_key][ref_stat]['avg_5-5']
                        ref_less25 = self.lg_strct[lg_key][ref_stat]['less_25']
                        ref_less15_25 = self.lg_strct[lg_key][ref_stat]['less_15-25']
                        ref_less5_15 = self.lg_strct[lg_key][ref_stat]['less_5-15']

                        ref_more = ref_more25 + ref_more15_25
                        ref_less15 = ref_less25 + ref_less15_25
                        ref_avg = ref_less15 + ref_less5_15 + ref_avg5_5
                        ref_less5 = ref_less15 + ref_less5_15

                        less5 = self.lg_strct[lg_key][stat]['less_5-15']
                        avg5_5 = self.lg_strct[lg_key][stat]['avg_5-5']
                        less = less25 + less15 + less5
                        avg = less + avg5_5

                        if team1_name in more25 and team2_name in more25 and ref_name in ref_more:
                            message_lst.append(f'STRONG_TOTAL_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif (team1_name in more25 and team2_name in more15 and ref_name in ref_more25) or (
                                team1_name in more15 and team2_name in more25 and ref_name in ref_more25):
                            message_lst.append(f'NORMAL_TOTAL_OVER_{stat}')
                            stat_viz_set.add(stat)

                        if team1_name in less25 and team2_name in less25 and ref_name in ref_avg:
                            message_lst.append(f'STRONG_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif (team1_name in less25 and team2_name in less15 and ref_name in ref_less5) or (
                                team1_name in less15 and team2_name in less25 and ref_name in ref_less5):
                            message_lst.append(f'NORMAL_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif team1_name in less and team2_name in less and ref_name in ref_less15:
                            message_lst.append(f'LOW_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif (team1_name in position_up_25 and team1_name in avg) and (
                                team2_name in position_down_25 and team2_name in avg) and ref_name in ref_avg:
                            message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        elif (team1_name in position_down_25 and team1_name in avg) and (
                                team2_name in position_up_25 and team2_name in avg) and ref_name in ref_avg:
                            message_lst.append(f'POSITION_TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team1_name in more25 and ref_name in ref_more:
                            message_lst.append(f'IND_1_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team1_name in less25 and ref_name in ref_less15:
                            message_lst.append(f'IND_1_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team2_name in more25 and ref_name in ref_more:
                            message_lst.append(f'IND_2_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team2_name in less25 and ref_name in ref_less15:
                            message_lst.append(f'IND_2_UNDER_{stat}')
                            stat_viz_set.add(stat)

        if message_lst and stat_viz_set:
            message = self.display_results(lg_key, team1_name, team2_name, "\n".join(message_lst))
            print(message)
            self.__plot_graphs(team1_name, team2_name, lg_key, stat_viz_set)
            matching_files = get_matching_files(ordered_file_list)
            await self.tel.send_message_with_files(message, *matching_files)
            time.sleep(3)

    def __plot_graphs(self, team1_name, team2_name, lg_key, stat_set):
        delete_files_in_folder(folder_path='graph/data')
        current_viz = TeamsStatsVisualizer(
            data=self.lg_data[lg_key],
            team_name_1=team1_name,
            team_name_2=team2_name)
        current_viz.plot_points(
            data_lst=self.lg_data[lg_key]['goals'],
            season='current_season')
        for stat in stat_set:
            current_viz.plot_team_stats(stat_key=stat,
                                        season='current_season',
                                        sort_by='avg_individual_team')
        time.sleep(3)

    def display_results(self, league, team1_name, team2_name, message):
        return f'''
########## LINE ##########
__League: {league}
ST Teams: {team1_name} - {team2_name}

{message}
'''


class LiveDataPreparer(GameStatAnalyzer):
    def __init__(self, lv_schedule: dict, lg_strct: dict, lg_data: dict):
        super().__init__(lv_schedule, lg_strct, lg_data)
        self.data = {'games': []}

    def run(self):
        for lg_dct in self.lv_schedule['data']:
            for game in lg_dct['match_data']:
                try:
                    self.analyze(game['team1_name'],
                                 game['team2_name'],
                                 game['ref_name'],
                                 lg_dct['league'])
                except ValueError:
                    continue

    def find_position(self, team1_name, team2_name, lg_key, result):
        position_groups = [
            self.lg_strct[lg_key]['position']['more_25'],
            self.lg_strct[lg_key]['position']['more_15-25'],
            self.lg_strct[lg_key]['position']['more_5-15'],
            self.lg_strct[lg_key]['position']['avg_5-5'],
            self.lg_strct[lg_key]['position']['less_5-15'],
            self.lg_strct[lg_key]['position']['less_15-25'],
            self.lg_strct[lg_key]['position']['less_25']
        ]

        team1_group = None
        team2_group = None

        for i, group in enumerate(position_groups):
            if team1_name in group:
                team1_group = i
            if team2_name in group:
                team2_group = i

        if team1_group is None or team2_group is None:
            raise ValueError("Одна или обе команды отсутствуют в группах.")

        if team1_group < team2_group:
            result['team1_pos'] = 'over'
            result['team2_pos'] = 'under'
        elif team1_group > team2_group:
            result['team1_pos'] = 'under'
            result['team2_pos'] = 'over'
        else:
            result['team1_pos'] = 'equal'
            result['team2_pos'] = 'equal'

        result['league'] = lg_key
        result['team1_name'] = team1_name
        result['team2_name'] = team2_name
        return result

    def analyze(self, team1_name, team2_name, ref_name, lg_key):
        try:
            lg_strct = self.lg_strct[lg_key]
        except KeyError:
            return
        result = {}
        self.find_position(team1_name, team2_name, lg_key, result)
        stat_viz_set = set()

        for stat in lg_strct:
            if stat not in ['goals', 'ref_yellow cards', 'ref_fouls', 'position']:
                message_lst = []
                more25 = self.lg_strct[lg_key][stat]['more_25']
                more15 = self.lg_strct[lg_key][stat]['more_15-25']
                less25 = self.lg_strct[lg_key][stat]['less_25']
                less15 = self.lg_strct[lg_key][stat]['less_15-25']
                more = more25 + more15
                less = less25 + less15

                if team1_name in more and team2_name in less:
                    message_lst.append(f'HANDICAP1_{stat}')
                    stat_viz_set.add(stat)

                elif team1_name in less and team2_name in more:
                    message_lst.append(f'HANDICAP2_{stat}')
                    stat_viz_set.add(stat)

                if stat in ['yellow cards', 'fouls']:
                    if ref_name:
                        ref_stat = 'ref_' + stat
                        try:
                            ref_more25 = self.lg_strct[lg_key][ref_stat]['more_25']
                        except KeyError:
                            continue
                        ref_more15_25 = self.lg_strct[lg_key][ref_stat]['more_15-25']
                        ref_less25 = self.lg_strct[lg_key][ref_stat]['less_25']
                        ref_less15_25 = self.lg_strct[lg_key][ref_stat]['less_15-25']
                        ref_less5_15 = self.lg_strct[lg_key][ref_stat]['less_5-15']

                        ref_more = ref_more25 + ref_more15_25
                        ref_less = ref_less25 + ref_less15_25 + ref_less5_15

                        if team1_name in more and team2_name in more and ref_name in ref_more:
                            message_lst.append(f'TOTAL_OVER_{stat}')
                            stat_viz_set.add(stat)
                        if team1_name in less and team2_name in less and ref_name in ref_less:
                            message_lst.append(f'TOTAL_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team1_name in more and ref_name in ref_more:
                            message_lst.append(f'IND1_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team1_name in less and ref_name in ref_less:
                            message_lst.append(f'IND1_UNDER_{stat}')
                            stat_viz_set.add(stat)

                        if team2_name in more and ref_name in ref_more:
                            message_lst.append(f'IND2_OVER_{stat}')
                            stat_viz_set.add(stat)
                        elif team2_name in less and ref_name in ref_less:
                            message_lst.append(f'IND2_UNDER_{stat}')
                            stat_viz_set.add(stat)

                else:
                    if team1_name in more and team2_name in more:
                        message_lst.append(f'TOTAL_OVER_{stat}')
                        stat_viz_set.add(stat)
                    if team1_name in less and team2_name in less:
                        message_lst.append(f'TOTAL_UNDER_{stat}')
                        stat_viz_set.add(stat)

                    if team1_name in more:
                        message_lst.append(f'IND1_OVER_{stat}')
                        stat_viz_set.add(stat)
                    elif team1_name in less:
                        message_lst.append(f'IND1_UNDER_{stat}')
                        stat_viz_set.add(stat)

                    if team2_name in more:
                        message_lst.append(f'IND2_OVER_{stat}')
                        stat_viz_set.add(stat)
                    elif team2_name in less:
                        message_lst.append(f'IND2_UNDER_{stat}')
                        stat_viz_set.add(stat)

                if message_lst:
                    result[stat] = "\n".join(message_lst)

        result['stat_set'] = stat_viz_set
        self.data['games'].append(result)
