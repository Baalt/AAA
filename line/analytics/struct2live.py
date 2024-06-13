import os
import time

from graph.matrix_stats_viz import ScatterPlotBuilder
from graph.teams_stats_viz import TeamsStatsVisualizer
from line.analytics.live_utils.total import LiveTotalCalculation
from line.analytics.message_builder import LiveMessageBuilder
from line.analytics.structures import HomeDataStructure, AwayDataStructure
from line.analytics.line_utils.stat_math import StatMath
from utils.stat_switcher import stats_dict


class FromStructureToLiveDict(LiveTotalCalculation, StatMath):
    @property
    def get_data(self):
        return self.main_data

    async def calculate(self,
                        home_structure: HomeDataStructure,
                        away_structure: AwayDataStructure,
                        statistic_name: str):
        if statistic_name in ['ЖК', 'Фолы'] and self.referee_data[statistic_name]['count'] > 5:
            try:
                ref_all_under_t = self.search_under_total(seq=self.referee_data[statistic_name]['all'], ref=True)
            except KeyError:
                ref_all_under_t = None
            try:
                ref_15_under_t = self.search_under_total(
                    seq=self.referee_data[statistic_name]['first_15_elements'],
                    ref=True)
            except KeyError:
                ref_15_under_t = None

            if ref_15_under_t:
                ref_all_under_p = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['all'],
                    total=ref_all_under_t)
                ref_15_under_p = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['first_15_elements'],
                    total=ref_15_under_t)
                ref_all_under_p1 = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['all'],
                    total=ref_all_under_t + 1)
                ref_15_under_p1 = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['first_15_elements'],
                    total=ref_15_under_t + 1)
                ref_all_under_p2 = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['all'],
                    total=ref_all_under_t + 2)
                ref_15_under_p2 = self.calculate_percent_by_total(
                    seq=self.referee_data[statistic_name]['first_15_elements'],
                    total=ref_15_under_t + 2)

                last_year_home_t = \
                    self.search_under_total(seq=home_structure.last_year_total_current_home_command_in_home_away_games,
                                            percent=90)
                len_under_year_1 = len(home_structure.last_year_total_current_home_command_in_home_away_games)
                last_year_away_t = \
                    self.search_under_total(seq=away_structure.last_year_total_current_away_command_in_home_away_games,
                                            percent=90)
                len_under_year_2 = len(away_structure.last_year_total_current_away_command_in_home_away_games)
                high_similar_home_t = \
                    self.search_under_total(
                        seq=home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                        percent=90)
                len_under_sim_1 = len(home_structure.similar_command_total_current_home_big_data_home_away_games_high)
                high_similar_away_t = \
                    self.search_under_total(
                        seq=away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                        percent=90)
                low_similar_home_t = \
                    self.search_under_total(
                        seq=home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                        percent=90)
                len_under_sim_2 = len(home_structure.similar_command_total_current_home_big_data_home_away_games_low)
                low_similar_away_t = \
                    self.search_under_total(
                        seq=away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                        percent=90)
                last_20_home_t = \
                    self.search_under_total(
                        seq=home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                        percent=90)
                len_under_20_1 = len(home_structure.last_20_games_total_current_home_by_year_in_home_away_games)
                last_20_away_t = \
                    self.search_under_total(
                        seq=away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                        percent=90)
                len_under_20_2 = len(away_structure.last_20_games_total_current_away_by_year_in_home_away_games)
                last_12_home_t = \
                    self.search_under_total(
                        seq=home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:12],
                        percent=90)
                len_under_ha_1 = len(home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:12])
                last_12_away_t = \
                    self.search_under_total(
                        seq=away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12],
                        percent=90)
                len_under_ha_2 = len(away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12])

                under_list_year_t = [last_year_home_t, last_year_away_t]
                under_list_sim_t = [high_similar_home_t, high_similar_away_t,
                                    low_similar_home_t, low_similar_away_t]
                under_list_20_t = [last_20_home_t, last_20_away_t]
                under_list_ha_t = [last_12_home_t, last_12_away_t]

                try:
                    under_year_t = max([var for var in under_list_year_t if var is not None])
                    under_sim_t = max([var for var in under_list_sim_t if var is not None])
                    under_20_t = max([var for var in under_list_20_t if var is not None])
                    under_ha_t = max([var for var in under_list_ha_t if var is not None])
                except ValueError:
                    return

                under_year_home_p = self.calculate_percent_by_total(
                    seq=home_structure.last_year_total_current_home_command_in_home_away_games,
                    total=under_year_t)
                under_year_away_p = self.calculate_percent_by_total(
                    seq=away_structure.last_year_total_current_away_command_in_home_away_games,
                    total=under_year_t)
                under_year_home_p1 = self.calculate_percent_by_total(
                    seq=home_structure.last_year_total_current_home_command_in_home_away_games,
                    total=under_year_t + 1)
                under_year_away_p1 = self.calculate_percent_by_total(
                    seq=away_structure.last_year_total_current_away_command_in_home_away_games,
                    total=under_year_t + 1)
                under_year_home_p2 = self.calculate_percent_by_total(
                    seq=home_structure.last_year_total_current_home_command_in_home_away_games,
                    total=under_year_t + 2)
                under_year_away_p2 = self.calculate_percent_by_total(
                    seq=away_structure.last_year_total_current_away_command_in_home_away_games,
                    total=under_year_t + 2)

                high_under_sim_home_p = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                    total=under_sim_t)
                high_under_sim_away_p = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                    total=under_sim_t)
                low_under_sim_home_p = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                    total=under_sim_t)
                low_under_sim_away_p = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                    total=under_sim_t)
                high_under_sim_home_p1 = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                    total=under_sim_t + 1)
                high_under_sim_away_p1 = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                    total=under_sim_t + 1)
                low_under_sim_home_p1 = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                    total=under_sim_t + 1)
                low_under_sim_away_p1 = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                    total=under_sim_t + 1)
                high_under_sim_home_p2 = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_high,
                    total=under_sim_t + 2)
                high_under_sim_away_p2 = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_high,
                    total=under_sim_t + 2)
                low_under_sim_home_p2 = self.calculate_percent_by_total(
                    seq=home_structure.similar_command_total_current_home_big_data_home_away_games_low,
                    total=under_sim_t + 2)
                low_under_sim_away_p2 = self.calculate_percent_by_total(
                    seq=away_structure.similar_command_total_current_away_big_data_home_away_games_low,
                    total=under_sim_t + 2)

                under_20_home_p = self.calculate_percent_by_total(
                    seq=home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                    total=under_20_t)
                under_20_away_p = self.calculate_percent_by_total(
                    seq=away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                    total=under_20_t)
                under_20_home_p1 = self.calculate_percent_by_total(
                    seq=home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                    total=under_20_t + 1)
                under_20_away_p1 = self.calculate_percent_by_total(
                    seq=away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                    total=under_20_t + 1)
                under_20_home_p2 = self.calculate_percent_by_total(
                    seq=home_structure.last_20_games_total_current_home_by_year_in_home_away_games,
                    total=under_20_t + 2)
                under_20_away_p2 = self.calculate_percent_by_total(
                    seq=away_structure.last_20_games_total_current_away_by_year_in_home_away_games,
                    total=under_20_t + 2)

                under_ha_home_p = self.calculate_percent_by_total(
                    seq=home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:12],
                    total=under_ha_t)
                under_ha_away_p = self.calculate_percent_by_total(
                    seq=away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12],
                    total=under_ha_t)
                under_ha_home_p1 = self.calculate_percent_by_total(
                    seq=home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:12],
                    total=under_ha_t + 1)
                under_ha_away_p1 = self.calculate_percent_by_total(
                    seq=away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12],
                    total=under_ha_t + 1)
                under_ha_home_p2 = self.calculate_percent_by_total(
                    seq=home_structure.last_12_games_total_current_home_command_by_year_in_home_games[:12],
                    total=under_ha_t + 2)
                under_ha_away_p2 = self.calculate_percent_by_total(
                    seq=away_structure.last_12_games_total_current_away_command_by_year_in_away_games[:12],
                    total=under_ha_t + 2)

                under_list_year_p = [under_year_home_p, under_year_away_p]
                under_list_year_p1 = [under_year_home_p1, under_year_away_p1]
                under_list_year_p2 = [under_year_home_p2, under_year_away_p2]

                under_list_sim_p = [high_under_sim_home_p, high_under_sim_away_p,
                                    low_under_sim_home_p, low_under_sim_away_p]
                under_list_sim_p1 = [high_under_sim_home_p1, high_under_sim_away_p1,
                                     low_under_sim_home_p1, low_under_sim_away_p1]
                under_list_sim_p2 = [high_under_sim_home_p2, high_under_sim_away_p2,
                                     low_under_sim_home_p2, low_under_sim_away_p2]
                under_list_20_p = [under_20_home_p, under_20_away_p]
                under_list_20_p1 = [under_20_home_p1, under_20_away_p1]
                under_list_20_p2 = [under_20_home_p2, under_20_away_p2]

                under_list_ha_p = [under_ha_home_p, under_ha_away_p]
                under_list_ha_p1 = [under_ha_home_p1, under_ha_away_p1]
                under_list_ha_p2 = [under_ha_home_p2, under_ha_away_p2]

                under_year_p = min([var for var in under_list_year_p if var is not None])
                under_year_p1 = min([var for var in under_list_year_p1 if var is not None])
                under_year_p2 = min([var for var in under_list_year_p2 if var is not None])

                under_sim_p = min([var for var in under_list_sim_p if var is not None])
                under_sim_p1 = min([var for var in under_list_sim_p1 if var is not None])
                under_sim_p2 = min([var for var in under_list_sim_p2 if var is not None])

                under_20_p = min([var for var in under_list_20_p if var is not None])
                under_20_p1 = min([var for var in under_list_20_p1 if var is not None])
                under_20_p2 = min([var for var in under_list_20_p2 if var is not None])

                under_ha_p = min([var for var in under_list_ha_p if var is not None])
                under_ha_p1 = min([var for var in under_list_ha_p1 if var is not None])
                under_ha_p2 = min([var for var in under_list_ha_p2 if var is not None])

                live_dict = {stats_dict[statistic_name]: {'ref_all_under_t': ref_all_under_t,
                                                          'ref_all_under_p': ref_all_under_p,
                                                          'ref_all_under_t1': ref_all_under_t + 1,
                                                          'ref_all_under_p1': ref_all_under_p1,
                                                          'ref_all_under_t2': ref_all_under_t + 2,
                                                          'ref_all_under_p2': ref_all_under_p2,
                                                          'ref_15_under_t': ref_15_under_t,
                                                          'ref_15_under_p': ref_15_under_p,
                                                          'ref_15_under_t1': ref_15_under_t + 1,
                                                          'ref_15_under_p1': ref_15_under_p1,
                                                          'ref_15_under_t2': ref_15_under_t + 2,
                                                          'ref_15_under_p2': ref_15_under_p2,
                                                          'ref_all_len': self.referee_data[statistic_name]['count'],
                                                          'ref_avg': self.referee_data[statistic_name]['avg'],
                                                          'under_year_t': under_year_t,
                                                          'under_year_t1': under_year_t + 1,
                                                          'under_year_t2': under_year_t + 2,
                                                          'under_sim_t': under_sim_t,
                                                          'under_sim_t1': under_sim_t + 1,
                                                          'under_sim_t2': under_sim_t + 2,
                                                          'under_20_t': under_20_t,
                                                          'under_20_t1': under_20_t + 1,
                                                          'under_20_t2': under_20_t + 2,
                                                          'under_ha_t': under_ha_t,
                                                          'under_ha_t1': under_ha_t + 1,
                                                          'under_ha_t2': under_ha_t + 2,
                                                          'under_year_p': under_year_p,
                                                          'under_year_p1': under_year_p1,
                                                          'under_year_p2': under_year_p2,
                                                          'under_sim_p': under_sim_p,
                                                          'under_sim_p1': under_sim_p1,
                                                          'under_sim_p2': under_sim_p2,
                                                          'under_20_p': under_20_p,
                                                          'under_20_p1': under_20_p1,
                                                          'under_20_p2': under_20_p2,
                                                          'under_ha_p': under_ha_p,
                                                          'under_ha_p1': under_ha_p1,
                                                          'under_ha_p2': under_ha_p2,
                                                          'len_under_year_1': len_under_year_1,
                                                          'len_under_year_2': len_under_year_2,
                                                          'len_under_sim_1': len_under_sim_1,
                                                          'len_under_sim_2': len_under_sim_2,
                                                          'len_under_20_1': len_under_20_1,
                                                          'len_under_20_2': len_under_20_2,
                                                          'len_under_ha_1': len_under_ha_1,
                                                          'len_under_ha_2': len_under_ha_2,
                                                          }}
                self.main_data.update(live_dict)
                if not self.main_data['check']:
                    self.main_data['check'] = True

                # message = LiveMessageBuilder(league_name=self.league, referee_name=self.referee_name,
                #                              home_command_name=self.team1_name, away_command_name=self.team2_name,
                #                              live_dict=live_dict[stats_dict[statistic_name]],
                #                              statistic=stats_dict[statistic_name]).get_message()
                # print(message)
                # self.__plot_graphs(statistic_name=stats_dict[statistic_name], total=ref_15_under_t)
                # await self.telegram.send_message_with_files(message, *self.files)

    def __plot_graphs(self, statistic_name, total):
        self.delete_files_in_folder(folder_path='graph/data')
        current_viz = TeamsStatsVisualizer(
            data=self.league_data['current_season'],
            team_name_1=self.team1_name,
            team_name_2=self.team2_name)
        current_viz.plot_points(
            data_lst=self.league_data['current_season']['goals'],
            season='current_season')
        previous_viz = TeamsStatsVisualizer(
            data=self.league_data['previous_season'],
            team_name_1=self.team1_name,
            team_name_2=self.team2_name)
        previous_viz.plot_points(
            data_lst=self.league_data['previous_season']['goals'],
            season='previous_season')
        current_viz.plot_team_stats(stat_key=statistic_name, season='current_season',
                                    sort_by='avg_individual_team')
        previous_viz.plot_team_stats(stat_key=statistic_name, season='previous_season',
                                     sort_by='avg_individual_team')
        matrix_viz = ScatterPlotBuilder(matrix_data=self.year_matrix_data)
        matrix_viz.build_scatter_plot(stat_name=statistic_name,
                                      bookmaker_value=total,
                                      bet_direction='TU',
                                      season='year_current_season')
        matrix_viz.build_scatter_plot(stat_name=statistic_name,
                                      bookmaker_value=total,
                                      bet_direction='TU',
                                      season='year_previous_season')
        time.sleep(3)

    def delete_files_in_folder(self, folder_path):
        """
        Deletes all files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)
